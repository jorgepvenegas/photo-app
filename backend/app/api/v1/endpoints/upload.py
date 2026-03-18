from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
import uuid

from app.database import get_async_session
from app.models import Photo
from app.schemas import PresignedUrlRequest, PresignedUrlResponse, UploadConfirmRequest, PhotoRead
from app.api.v1.endpoints.auth import current_active_user
from app.services.storage import storage_service
from app.services.image import image_service

router = APIRouter()


@router.post("/presigned-url", response_model=PresignedUrlResponse)
async def get_presigned_url(
    request: PresignedUrlRequest,
    current_user = Depends(current_active_user)
):
    """Get presigned URL for direct upload to R2."""
    # Validate image type
    ext = request.filename.lower().split('.')[-1] if '.' in request.filename else ''
    if f'.{ext}' not in image_service.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(image_service.ALLOWED_EXTENSIONS)}"
        )
    
    # Validate file size
    if request.file_size > image_service.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max: {image_service.MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Generate presigned URL
    result = await storage_service.generate_presigned_upload_url(
        user_id=str(current_user.id),
        filename=request.filename,
        content_type=request.content_type
    )
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to generate upload URL")
    
    upload_url, storage_key, public_url = result
    
    return PresignedUrlResponse(
        upload_url=upload_url,
        storage_key=storage_key,
        expires_in=300
    )


@router.post("/confirm", response_model=PhotoRead)
async def confirm_upload(
    confirm: UploadConfirmRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    current_user = Depends(current_active_user)
):
    """Confirm upload and create photo record. Triggers thumbnail generation."""
    # Create photo record
    photo = Photo(
        user_id=current_user.id,
        title=confirm.title,
        description=confirm.description,
        storage_key=confirm.storage_key,
        storage_url=confirm.storage_key,
        mime_type=confirm.mime_type,
        file_size=confirm.file_size,
        width=confirm.width,
        height=confirm.height,
        is_public=confirm.is_public
    )
    
    session.add(photo)
    await session.commit()
    await session.refresh(photo)
    
    # Trigger thumbnail generation in background
    background_tasks.add_task(generate_thumbnails_task, photo.id, confirm.storage_key)
    
    return PhotoRead.model_validate(photo)


async def generate_thumbnails_task(photo_id: uuid.UUID, storage_key: str):
    """Background task to generate thumbnails and upload to R2."""
    import asyncio
    from app.database import async_session_maker
    from app.services.storage import storage_service

    await asyncio.sleep(2)

    try:
        original = await storage_service.download_file(storage_key)
        if not original:
            print(f"Failed to download original for photo {photo_id}")
            return

        key_dir = storage_key.rsplit('/', 1)[0]
        filename = storage_key.rsplit('/', 1)[-1].rsplit('.', 1)[0]

        async with async_session_maker() as session:
            query = select(Photo).where(Photo.id == photo_id)
            result = await session.execute(query)
            photo = result.scalar_one_or_none()
            if not photo:
                return

            for size_name, attr in [("small", "thumb_small_key"), ("medium", "thumb_medium_key"), ("large", "thumb_large_key")]:
                thumb_data = image_service.create_thumbnail(original, size_name)
                if thumb_data:
                    thumb_key = f"{key_dir}/thumb_{size_name}_{filename}.webp"
                    uploaded = await storage_service.upload_file(thumb_key, thumb_data)
                    if uploaded:
                        setattr(photo, attr, thumb_key)

            await session.commit()
            print(f"Thumbnails generated for photo {photo_id}")

    except Exception as e:
        print(f"Failed to generate thumbnails for photo {photo_id}: {e}")
