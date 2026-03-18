from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload
from typing import List
import uuid

from app.database import get_async_session
from app.models import Photo, Comment, User
from app.schemas import PhotoCreate, PhotoUpdate, PhotoRead, PhotoDetail, PhotoList
from app.api.v1.endpoints.auth import current_verified_user

router = APIRouter()


@router.get("", response_model=PhotoList)
async def list_photos(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    user_id: uuid.UUID = None,
    session: AsyncSession = Depends(get_async_session)
):
    """List public photos with pagination."""
    query = select(Photo).where(Photo.is_public == True).options(selectinload(Photo.user))
    
    if user_id:
        query = query.where(Photo.user_id == user_id)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await session.scalar(count_query)
    
    # Get paginated results
    offset = (page - 1) * per_page
    query = query.order_by(desc(Photo.created_at)).offset(offset).limit(per_page)
    
    result = await session.execute(query)
    photos = result.scalars().all()
    
    return PhotoList(
        photos=[PhotoRead.model_validate(p) for p in photos],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/me", response_model=PhotoList)
async def list_my_photos(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_verified_user)
):
    """List current user's photos."""
    query = select(Photo).where(Photo.user_id == current_user.id)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await session.scalar(count_query)
    
    # Get paginated results
    offset = (page - 1) * per_page
    query = query.order_by(desc(Photo.created_at)).offset(offset).limit(per_page)
    
    result = await session.execute(query)
    photos = result.scalars().all()
    
    return PhotoList(
        photos=[PhotoRead.model_validate(p) for p in photos],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/{photo_id}", response_model=PhotoDetail)
async def get_photo(
    photo_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_verified_user)
):
    """Get photo details."""
    query = select(Photo).where(Photo.id == photo_id).options(
        selectinload(Photo.user),
        selectinload(Photo.comments).selectinload(Comment.user)
    )
    result = await session.execute(query)
    photo = result.scalar_one_or_none()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    if not photo.is_public and photo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this photo")
    
    return PhotoDetail(
        **PhotoRead.model_validate(photo).model_dump(),
        user=photo.user,
        comments_count=len([c for c in photo.comments if not c.is_deleted])
    )


@router.put("/{photo_id}", response_model=PhotoRead)
async def update_photo(
    photo_id: uuid.UUID,
    photo_update: PhotoUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_verified_user)
):
    """Update photo metadata."""
    query = select(Photo).where(Photo.id == photo_id)
    result = await session.execute(query)
    photo = result.scalar_one_or_none()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    if photo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this photo")
    
    # Update fields
    update_data = photo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(photo, field, value)
    
    await session.commit()
    await session.refresh(photo)
    
    return PhotoRead.model_validate(photo)


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(
    photo_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_verified_user)
):
    """Delete photo and its thumbnails."""
    from app.services.storage import storage_service
    
    query = select(Photo).where(Photo.id == photo_id)
    result = await session.execute(query)
    photo = result.scalar_one_or_none()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    if photo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this photo")
    
    # Delete from storage
    keys_to_delete = [
        photo.storage_key,
        photo.thumb_small_key,
        photo.thumb_medium_key,
        photo.thumb_large_key
    ]
    
    for key in keys_to_delete:
        if key:
            await storage_service.delete_file(key)
    
    # Delete from database (cascades to comments)
    await session.delete(photo)
    await session.commit()
    
    return None
