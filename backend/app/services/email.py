from typing import Optional
import resend
from app.config import get_settings

settings = get_settings()

if settings.RESEND_API_KEY:
    resend.api_key = settings.RESEND_API_KEY


class EmailService:
    """Email service using Resend API."""
    
    @staticmethod
    async def send_verification_email(email: str, token: str) -> bool:
        """Send email verification link."""
        if not settings.RESEND_API_KEY:
            # In development, just print the token
            print(f"\n[DEV] Verification email to {email}: {settings.APP_URL}/verify-email?token={token}\n")
            return True
        
        try:
            verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
            
            resend.Emails.send({
                "from": settings.RESEND_FROM_EMAIL,
                "to": email,
                "subject": "Verify your PhotoApp account",
                "html": f"""
                <h1>Welcome to PhotoApp!</h1>
                <p>Please click the link below to verify your email address:</p>
                <a href="{verification_url}" style="padding: 10px 20px; background: #3b82f6; color: white; text-decoration: none; border-radius: 5px;">
                    Verify Email
                </a>
                <p>Or copy and paste this URL: {verification_url}</p>
                <p>This link expires in 24 hours.</p>
                """
            })
            return True
        except Exception as e:
            print(f"Failed to send verification email: {e}")
            return False
    
    @staticmethod
    async def send_password_reset_email(email: str, token: str) -> bool:
        """Send password reset link."""
        if not settings.RESEND_API_KEY:
            print(f"\n[DEV] Password reset email to {email}: {settings.FRONTEND_URL}/reset-password?token={token}\n")
            return True
        
        try:
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            
            resend.Emails.send({
                "from": settings.RESEND_FROM_EMAIL,
                "to": email,
                "subject": "Reset your PhotoApp password",
                "html": f"""
                <h1>Password Reset Request</h1>
                <p>Click the link below to reset your password:</p>
                <a href="{reset_url}" style="padding: 10px 20px; background: #ef4444; color: white; text-decoration: none; border-radius: 5px;">
                    Reset Password
                </a>
                <p>Or copy and paste this URL: {reset_url}</p>
                <p>This link expires in 1 hour.</p>
                <p>If you didn't request this, please ignore this email.</p>
                """
            })
            return True
        except Exception as e:
            print(f"Failed to send password reset email: {e}")
            return False


email_service = EmailService()
