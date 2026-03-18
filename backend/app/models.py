import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from app.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model with email verification support."""
    __tablename__ = "users"
    
    # Email verification fields (in addition to FastAPI-Users defaults)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_token = Column(String(255), nullable=True)
    verification_token_expires = Column(DateTime, nullable=True)
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    photos = relationship("Photo", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")


class Photo(Base):
    """Photo model with thumbnail support."""
    __tablename__ = "photos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Metadata
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Original file
    storage_key = Column(String(512), nullable=False)
    storage_url = Column(String(1024), nullable=False)
    mime_type = Column(String(128), nullable=False)
    file_size = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    
    # Thumbnails
    thumb_small_key = Column(String(512), nullable=True)   # 200px
    thumb_small_url = Column(String(1024), nullable=True)
    thumb_medium_key = Column(String(512), nullable=True)  # 800px
    thumb_medium_url = Column(String(1024), nullable=True)
    thumb_large_key = Column(String(512), nullable=True)   # 1600px
    thumb_large_url = Column(String(1024), nullable=True)
    
    # Visibility
    is_public = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="photos")
    comments = relationship("Comment", back_populates="photo", cascade="all, delete-orphan")


class Comment(Base):
    """Flat comment model (no nesting)."""
    __tablename__ = "comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    photo_id = Column(UUID(as_uuid=True), ForeignKey("photos.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    content = Column(Text, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    photo = relationship("Photo", back_populates="comments")
    user = relationship("User", back_populates="comments")
