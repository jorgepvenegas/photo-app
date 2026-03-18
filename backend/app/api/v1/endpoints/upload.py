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
        storage_url=storage_service._get_public_url(confirm.storage_key),
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
    
    # Wait a moment for the file to be fully available in R2
    await asyncio.sleep(2)
    
    try:
        # Download original from R2
        # In production, this would download the file
        # For now, we'll skip this step since we need to implement download
        # This is a placeholder for the async thumbnail generation
        
        async with async_session_maker() as session:
            query = select(Photo).where(Photo.id == photo_id)
            result = await session.execute(query)
            photo = result.scalar_one_or_none()
            
            if not photo:
                return
            
            # For now, set placeholder URLs
            # In production, generate real thumbnails
            base_url = photo.storage_url.rsplit('/', 1)[0]
            filename = photo.storage_key.rsplit('/', 1)[-1].rsplit('.', 1)[0]
            
            photo.thumb_small_key = f"{photo.storage_key.rsplit('/', 1)[0]}/thumb_small_{filename}.webp"
            photo.thumb_small_url = f"{base_url}/thumb_small_{filename}.webp"
            
            photo.thumb_medium_key = f"{photo.storage_key.rsplit('/', 1)[0]}/thumb_medium_{filename}.webp"
            photo.thumb_medium_url = f"{base_url}/thumb_medium_{filename}.webp"
            
            photo.thumb_large_key = f"{photo.storage_key.rsplit('/', 1)[0]}/thumb_large_{filename}.webp"
            photo.thumb_large_url = f"{base_url}/thumb_large_{filename}.webp"
            
            await session.commit()
    
    except Exception as e:
        print(f"Failed to generate thumbnails for photo {photo_id}: {e}")
