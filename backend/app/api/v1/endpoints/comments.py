from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload
import uuid

from app.database import get_async_session
from app.models import Comment, Photo, User
from app.schemas import CommentCreate, CommentUpdate, CommentRead, CommentList
from app.api.v1.endpoints.auth import current_verified_user

router = APIRouter()


@router.get("/photos/{photo_id}/comments", response_model=CommentList)
async def list_comments(
    photo_id: uuid.UUID,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_verified_user)
):
    """Get comments for a photo."""
    # Check photo exists and is accessible
    photo_query = select(Photo).where(Photo.id == photo_id)
    photo_result = await session.execute(photo_query)
    photo = photo_result.scalar_one_or_none()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    if not photo.is_public and photo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view comments on this photo")
    
    # Get comments
    query = (
        select(Comment)
        .where(Comment.photo_id == photo_id, Comment.is_deleted == False)
        .options(selectinload(Comment.user))
        .order_by(desc(Comment.created_at))
    )
    
    # Get total count
    count_query = select(func.count()).select_from(
        query.where(Comment.is_deleted == False).subquery()
    )
    total = await session.scalar(count_query)
    
    # Paginate
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)
    
    result = await session.execute(query)
    comments = result.scalars().all()
    
    return CommentList(
        comments=[CommentRead.model_validate(c) for c in comments],
        total=total
    )


@router.post("/photos/{photo_id}/comments", response_model=CommentRead)
async def create_comment(
    photo_id: uuid.UUID,
    comment_data: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_verified_user)
):
    """Add a comment to a photo."""
    # Check photo exists
    photo_query = select(Photo).where(Photo.id == photo_id)
    photo_result = await session.execute(photo_query)
    photo = photo_result.scalar_one_or_none()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    if not photo.is_public and photo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to comment on this photo")
    
    # Validate content
    if not comment_data.content or len(comment_data.content.strip()) < 1:
        raise HTTPException(status_code=400, detail="Comment cannot be empty")
    
    if len(comment_data.content) > 2000:
        raise HTTPException(status_code=400, detail="Comment too long (max 2000 chars)")
    
    # Create comment
    comment = Comment(
        photo_id=photo_id,
        user_id=current_user.id,
        content=comment_data.content.strip()
    )
    
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    
    # Load user for response
    await session.refresh(comment, ['user'])
    
    return CommentRead.model_validate(comment)


@router.put("/{comment_id}", response_model=CommentRead)
async def update_comment(
    comment_id: uuid.UUID,
    comment_data: CommentUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_verified_user)
):
    """Update own comment."""
    query = select(Comment).where(Comment.id == comment_id).options(selectinload(Comment.user))
    result = await session.execute(query)
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    
    if comment.is_deleted:
        raise HTTPException(status_code=400, detail="Cannot update deleted comment")
    
    # Validate content
    if not comment_data.content or len(comment_data.content.strip()) < 1:
        raise HTTPException(status_code=400, detail="Comment cannot be empty")
    
    if len(comment_data.content) > 2000:
        raise HTTPException(status_code=400, detail="Comment too long (max 2000 chars)")
    
    comment.content = comment_data.content.strip()
    await session.commit()
    await session.refresh(comment)
    
    return CommentRead.model_validate(comment)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_verified_user)
):
    """Soft delete own comment."""
    query = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(query)
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    # Soft delete
    comment.is_deleted = True
    comment.content = "[deleted]"
    await session.commit()
    
    return None
