import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


# ===================== USER SCHEMAS =====================

class UserRead(BaseUser):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseUserCreate):
    email: EmailStr
    password: str


class UserUpdate(BaseUserUpdate):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserProfile(BaseModel):
    id: uuid.UUID
    email: EmailStr
    created_at: datetime
    photos_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)


# ===================== PHOTO SCHEMAS =====================

class PhotoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = True


class PhotoCreate(PhotoBase):
    pass


class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class PhotoRead(PhotoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    storage_url: str
    thumb_small_url: Optional[str] = None
    thumb_medium_url: Optional[str] = None
    thumb_large_url: Optional[str] = None
    width: int
    height: int
    file_size: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PhotoDetail(PhotoRead):
    user: UserRead
    comments_count: int = 0


class PhotoList(BaseModel):
    photos: List[PhotoRead]
    total: int
    page: int
    per_page: int


# ===================== UPLOAD SCHEMAS =====================

class PresignedUrlRequest(BaseModel):
    filename: str
    content_type: str
    file_size: int


class PresignedUrlResponse(BaseModel):
    upload_url: str
    fields: Optional[dict] = None
    storage_key: str
    expires_in: int = 300  # 5 minutes


class UploadConfirmRequest(BaseModel):
    storage_key: str
    title: str
    description: Optional[str] = None
    width: int
    height: int
    file_size: int
    mime_type: str
    is_public: bool = True


# ===================== COMMENT SCHEMAS =====================

class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str


class CommentRead(CommentBase):
    id: uuid.UUID
    photo_id: uuid.UUID
    user_id: uuid.UUID
    user: UserRead
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CommentList(BaseModel):
    comments: List[CommentRead]
    total: int
