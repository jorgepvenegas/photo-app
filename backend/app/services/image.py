import io
from typing import Tuple, Optional
from PIL import Image


class ImageService:
    """Image processing service using Pillow."""
    
    # Thumbnail sizes
    THUMB_SIZES = {
        'small': (200, 200),
        'medium': (800, 800),
        'large': (1600, 1600)
    }
    
    ALLOWED_FORMATS = {'JPEG', 'PNG', 'GIF', 'WEBP'}
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_DIMENSION = 4096
    
    @staticmethod
    def validate_image(file_content: bytes, filename: str) -> Tuple[bool, str]:
        """
        Validate image file.
        Returns: (is_valid, error_message)
        """
        # Check file size
        if len(file_content) > ImageService.MAX_FILE_SIZE:
            return False, f"File too large. Max size: {ImageService.MAX_FILE_SIZE / 1024 / 1024}MB"
        
        # Check extension
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        if f'.{ext}' not in ImageService.ALLOWED_EXTENSIONS:
            return False, f"Invalid file type. Allowed: {', '.join(ImageService.ALLOWED_EXTENSIONS)}"
        
        try:
            # Try to open with Pillow
            img = Image.open(io.BytesIO(file_content))
            
            # Check format
            if img.format not in ImageService.ALLOWED_FORMATS:
                return False, f"Invalid image format: {img.format}. Allowed: {', '.join(ImageService.ALLOWED_FORMATS)}"
            
            # Check dimensions
            width, height = img.size
            if width > ImageService.MAX_DIMENSION or height > ImageService.MAX_DIMENSION:
                return False, f"Image too large. Max dimension: {ImageService.MAX_DIMENSION}px"
            
            if width < 10 or height < 10:
                return False, "Image too small. Minimum: 10x10px"
            
            return True, ""
        
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    @staticmethod
    def get_image_info(file_content: bytes) -> Tuple[int, int, str, int]:
        """
        Get image dimensions and info.
        Returns: (width, height, format, file_size)
        """
        img = Image.open(io.BytesIO(file_content))
        width, height = img.size
        format_type = img.format or 'JPEG'
        return width, height, format_type, len(file_content)
    
    @staticmethod
    def create_thumbnail(file_content: bytes, size_name: str) -> Optional[bytes]:
        """
        Create thumbnail from image.
        size_name: 'small', 'medium', or 'large'
        """
        try:
            max_size = ImageService.THUMB_SIZES.get(size_name)
            if not max_size:
                return None
            
            img = Image.open(io.BytesIO(file_content))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Calculate new size maintaining aspect ratio
            width, height = img.size
            ratio = min(max_size[0] / width, max_size[1] / height)
            new_size = (int(width * ratio), int(height * ratio))
            
            # Resize using high-quality downsampling
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Strip EXIF data for privacy
            # Already done by creating new image
            
            # Save to bytes
            output = io.BytesIO()
            
            # Use JPEG for smaller size, WEBP for better quality/compression
            img.save(output, format='WEBP', quality=85, optimize=True)
            output.seek(0)
            
            return output.getvalue()
        
        except Exception as e:
            print(f"Failed to create thumbnail: {e}")
            return None
    
    @staticmethod
    def strip_exif(file_content: bytes) -> bytes:
        """Remove EXIF data from image for privacy."""
        try:
            img = Image.open(io.BytesIO(file_content))
            
            # Create new image without EXIF
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            output = io.BytesIO()
            img.save(output, format=img.format or 'JPEG')
            output.seek(0)
            
            return output.getvalue()
        except:
            return file_content


image_service = ImageService()
