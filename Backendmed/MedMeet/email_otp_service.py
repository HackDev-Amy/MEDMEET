"""
Email-based OTP Service Module
Handles generating and sending OTP via Email (FREE & EASY)
No paid services required!
"""

import random
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from decouple import config
import logging

logger = logging.getLogger(__name__)


def generate_otp(length: int = None) -> str:
    """
    Generate random OTP code
    
    Args:
        length: Length of OTP (default from settings or 6)
    
    Returns:
        str: 6-digit OTP code
    """
    if length is None:
        length = int(config('OTP_LENGTH', 6))
    return ''.join(random.choices(string.digits, k=length))


def send_otp_email(email: str, otp_code: str) -> bool:
    """
    Send OTP via Email - Fully Functional!
    
    Args:
        email: Recipient email address
        otp_code: 6-digit OTP code
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        subject = "Your MedMeet OTP Code"
        
        html_message = f"""
        <html style="font-family: Arial, sans-serif;">
            <body style="background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    
                    <h2 style="color: #2c3e50; text-align: center;">MedMeet OTP Verification</h2>
                    
                    <p style="color: #555; font-size: 16px;">Hello,</p>
                    
                    <p style="color: #555; font-size: 16px;">Your OTP code for MedMeet login is:</p>
                    
                    <div style="background-color: #3498db; padding: 20px; text-align: center; border-radius: 8px; margin: 30px 0;">
                        <p style="font-size: 48px; font-weight: bold; color: white; margin: 0; letter-spacing: 10px;">
                            {otp_code}
                        </p>
                    </div>
                    
                    <p style="color: #e74c3c; font-size: 14px; text-align: center;">
                        ⏱️ This code will expire in <strong>10 minutes</strong>
                    </p>
                    
                    <hr style="border: none; border-top: 2px solid #ecf0f1; margin: 30px 0;">
                    
                    <p style="color: #555; font-size: 14px;">
                        <strong>Security Tip:</strong> Never share your OTP with anyone. 
                        MedMeet staff will never ask for your OTP.
                    </p>
                    
                    <p style="color: #555; font-size: 14px;">
                        If you didn't request this code, please ignore this email.
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 30px 0;">
                    
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        Best regards,<br>
                        <strong>MedMeet Team</strong><br>
                        <a href="http://localhost:8000" style="color: #3498db; text-decoration: none;">Visit MedMeet</a>
                    </p>
                    
                </div>
            </body>
        </html>
        """
        
        plain_message = f"""
Hello,

Your OTP code for MedMeet login is: {otp_code}

This code will expire in 10 minutes.

Security Tip: Never share your OTP with anyone. MedMeet staff will never ask for your OTP.

If you didn't request this code, please ignore this email.

Best regards,
MedMeet Team
        """
        
        # Send email
        send_mail(
            subject,
            plain_message,
            config('EMAIL_HOST_USER', settings.DEFAULT_FROM_EMAIL),
            [email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"OTP email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {e}")
        return False


def validate_otp(otp_obj, entered_otp: str) -> tuple:
    """
    Validate OTP code
    
    Args:
        otp_obj: OTP database object
        entered_otp: OTP code entered by user
    
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if otp_obj.is_used:
        return False, "OTP already used. Please request a new one."
    
    if otp_obj.is_expired():
        return False, "OTP has expired. Please request a new one."
    
    if otp_obj.otp_code != entered_otp:
        return False, "Invalid OTP code. Please try again."
    
    return True, "OTP verified successfully"
