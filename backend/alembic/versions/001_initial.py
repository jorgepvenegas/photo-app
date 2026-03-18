"""Initial migration - create users, photos, and comments tables.

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('verification_token', sa.String(length=255), nullable=True),
        sa.Column('verification_token_expires', sa.DateTime(), nullable=True),
        sa.Column('reset_token', sa.String(length=255), nullable=True),
        sa.Column('reset_token_expires', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    
    # Create photos table
    op.create_table(
        'photos',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('storage_key', sa.String(length=512), nullable=False),
        sa.Column('storage_url', sa.String(length=1024), nullable=False),
        sa.Column('mime_type', sa.String(length=128), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('width', sa.Integer(), nullable=False),
        sa.Column('height', sa.Integer(), nullable=False),
        sa.Column('thumb_small_key', sa.String(length=512), nullable=True),
        sa.Column('thumb_small_url', sa.String(length=1024), nullable=True),
        sa.Column('thumb_medium_key', sa.String(length=512), nullable=True),
        sa.Column('thumb_medium_url', sa.String(length=1024), nullable=True),
        sa.Column('thumb_large_key', sa.String(length=512), nullable=True),
        sa.Column('thumb_large_url', sa.String(length=1024), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_photos_user_id', 'photos', ['user_id'])
    op.create_index('ix_photos_created_at', 'photos', ['created_at'])
    
    # Create comments table
    op.create_table(
        'comments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('photo_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['photo_id'], ['photos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_comments_photo_id', 'comments', ['photo_id'])
    op.create_index('ix_comments_user_id', 'comments', ['user_id'])
    op.create_index('ix_comments_created_at', 'comments', ['created_at'])


def downgrade() -> None:
    op.drop_index('ix_comments_created_at', table_name='comments')
    op.drop_index('ix_comments_user_id', table_name='comments')
    op.drop_index('ix_comments_photo_id', table_name='comments')
    op.drop_table('comments')
    
    op.drop_index('ix_photos_created_at', table_name='photos')
    op.drop_index('ix_photos_user_id', table_name='photos')
    op.drop_table('photos')
    
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
