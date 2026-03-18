import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import Optional, Tuple
import uuid
from datetime import datetime, timedelta

from app.config import get_settings

settings = get_settings()


class StorageService:
    """Cloudflare R2 (S3-compatible) storage service."""
    
    def __init__(self):
        self.client = None
        self.bucket = settings.R2_BUCKET_NAME
        if settings.R2_ENDPOINT and settings.R2_ACCESS_KEY_ID and settings.R2_SECRET_ACCESS_KEY:
            self.client = boto3.client(
                's3',
                endpoint_url=settings.R2_ENDPOINT,
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
                config=Config(signature_version='s3v4')
            )
    
    def _generate_key(self, user_id: str, filename: str) -> str:
        """Generate unique storage key."""
        timestamp = datetime.utcnow().strftime('%Y/%m/%d')
        unique_id = str(uuid.uuid4())[:8]
        ext = filename.split('.')[-1].lower() if '.' in filename else 'jpg'
        return f"uploads/{user_id}/{timestamp}/{unique_id}.{ext}"
    
    def _get_public_url(self, key: str) -> str:
        """Get public URL for stored object."""
        if settings.R2_PUBLIC_URL:
            return f"{settings.R2_PUBLIC_URL}/{key}"
        return f"{settings.R2_ENDPOINT}/{self.bucket}/{key}"
    
    async def generate_presigned_upload_url(
        self, 
        user_id: str, 
        filename: str, 
        content_type: str,
        expires_in: int = 300
    ) -> Optional[Tuple[str, str, str]]:
        """
        Generate presigned URL for direct upload.
        Returns: (upload_url, storage_key, public_url)
        """
        if not self.client:
            # Dev mode - return mock values
            key = self._generate_key(str(user_id), filename)
            return (f"http://localhost:8000/mock-upload/{key}", key, f"http://localhost:8000/static/{key}")
        
        try:
            key = self._generate_key(str(user_id), filename)
            
            params = {
                'Bucket': self.bucket,
                'Key': key,
                'ContentType': content_type
            }
            
            url = self.client.generate_presigned_url(
                'put_object',
                Params=params,
                ExpiresIn=expires_in
            )
            
            public_url = self._get_public_url(key)
            return (url, key, public_url)
        
        except ClientError as e:
            print(f"Failed to generate presigned URL: {e}")
            return None
    
    async def delete_file(self, key: str) -> bool:
        """Delete file from storage."""
        if not self.client:
            print(f"[DEV] Would delete: {key}")
            return True
        
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError as e:
            print(f"Failed to delete file: {e}")
            return False
    
    async def generate_presigned_download_url(self, key: str, expires_in: int = 3600) -> Optional[str]:
        """Generate temporary download URL."""
        if not self.client:
            return f"http://localhost:8000/static/{key}"
        
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            print(f"Failed to generate download URL: {e}")
            return None


storage_service = StorageService()
