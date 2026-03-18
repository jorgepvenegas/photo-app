import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager, UUIDIDMixin

from app.database import get_async_session
from app.models import User
from app.config import get_settings
from app.services.email import email_service
from app.schemas import UserRead, UserCreate, UserUpdate

settings = get_settings()
router = APIRouter()

# User manager with email verification
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY
    reset_password_token_lifetime_seconds = 3600  # 1 hour
    verification_token_lifetime_seconds = 86400   # 24 hours
    
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        # Send verification email
        await self.request_verify(user)
    
    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        await email_service.send_password_reset_email(user.email, token)
    
    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        await email_service.send_verification_email(user.email, token)
    
    async def on_after_verify(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has verified their email.")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


# JWT authentication
bearer_transport = BearerTransport(tokenUrl="api/v1/auth/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI Users instance
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

# Dependency to get current user
current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)
current_optional_user = fastapi_users.current_user(active=True, verified=True, optional=True)


# Include FastAPI Users routers (they already have their own prefixes)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["users"],
)


@router.get("/me", response_model=UserRead, tags=["auth"])
async def get_me(user: User = Depends(current_active_user)):
    """Get current user info."""
    return user


@router.post("/logout", tags=["auth"])
async def logout():
    """Logout - client should clear token."""
    return {"message": "Logged out successfully"}
