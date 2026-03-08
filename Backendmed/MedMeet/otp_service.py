"""
OTP Service Module
Handles generating, storing, and sending OTP via SMS/Email
Supports multiple SMS providers: Twilio, AWS SNS, Mock(testing)
"""

import random
import string
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from decouple import config
import logging

logger = logging.getLogger(__name__)


class SMSProvider:
    """Base SMS Provider Class"""
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        raise NotImplementedError


class TwilioSMSProvider(SMSProvider):
    """Twilio SMS Provider"""
    
    def __init__(self):
        try:
            from twilio.rest import Client
            self.client = Client(
                config('TWILIO_ACCOUNT_SID'),
                config('TWILIO_AUTH_TOKEN')
            )
            self.from_number = config('TWILIO_PHONE_NUMBER')
        except Exception as e:
            logger.error(f"Twilio initialization failed: {e}")
            self.client = None
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send SMS via Twilio"""
        try:
            if not self.client:
                logger.error("Twilio client not initialized")
                return False
            
            msg = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=phone_number
            )
            logger.info(f"SMS sent to {phone_number} via Twilio. SID: {msg.sid}")
            return True
        except Exception as e:
            logger.error(f"Twilio SMS sending failed: {e}")
            return False


class AWSSNSProvider(SMSProvider):
    """AWS SNS SMS Provider"""
    
    def __init__(self):
        try:
            import boto3
            self.sns = boto3.client(
                'sns',
                region_name=config('AWS_REGION', 'us-east-1'),
                aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
            )
        except Exception as e:
            logger.error(f"AWS SNS initialization failed: {e}")
            self.sns = None
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send SMS via AWS SNS"""
        try:
            if not self.sns:
                logger.error("AWS SNS client not initialized")
                return False
            
            response = self.sns.publish(
                PhoneNumber=phone_number,
                Message=message,
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': 'MedMeet'
                    }
                }
            )
            logger.info(f"SMS sent to {phone_number} via AWS SNS. MessageId: {response['MessageId']}")
            return True
        except Exception as e:
            logger.error(f"AWS SNS SMS sending failed: {e}")
            return False


class MockSMSProvider(SMSProvider):
    """Mock SMS Provider for Testing - Logs to console instead of sending"""
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """Log SMS to console (for testing)"""
        logger.warning(f"[MOCK SMS] To: {phone_number}")
        logger.warning(f"[MOCK SMS] Message: {message}")
        print(f"\n{'='*60}")
        print(f"[MOCK SMS - TEST MODE]")
        print(f"Phone: {phone_number}")
        print(f"Message: {message}")
        print(f"{'='*60}\n")
        return True


class EmailProvider:
    """Email Provider for OTP delivery (fallback option)"""
    
    @staticmethod
    def send_otp_email(email: str, otp_code: str, phone_number: str) -> bool:
        """Send OTP via email"""
        try:
            subject = "Your MedMeet OTP Code"
            message = f"""
Hello,

Your OTP code for MedMeet login is: {otp_code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
MedMeet Team
            """
            send_mail(
                subject,
                message,
                config('EMAIL_HOST_USER', 'noreply@medmeet.com'),
                [email],
                fail_silently=False,
            )
            logger.info(f"OTP email sent to {email} for phone {phone_number}")
            return True
        except Exception as e:
            logger.error(f"Failed to send OTP email: {e}")
            return False


def get_sms_provider() -> SMSProvider:
    """Get configured SMS provider instance"""
    provider_name = config('SMS_PROVIDER', 'MOCK').upper()
    
    if provider_name == 'TWILIO':
        return TwilioSMSProvider()
    elif provider_name == 'AWS_SNS':
        return AWSSNSProvider()
    else:  # Default to MOCK
        return MockSMSProvider()


def send_otp_sms(phone_number: str, otp_code: str) -> bool:
    """
    Send OTP via SMS
    
    Args:
        phone_number: Recipient phone number
        otp_code: 6-digit OTP code
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    provider = get_sms_provider()
    message = f"Your MedMeet OTP is: {otp_code}. Valid for 10 minutes."
    return provider.send_sms(phone_number, message)


def send_otp_email(email: str, otp_code: str, phone_number: str) -> bool:
    """
    Send OTP via Email (fallback)
    
    Args:
        email: Recipient email
        otp_code: 6-digit OTP code
        phone_number: Associated phone number
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    return EmailProvider.send_otp_email(email, otp_code, phone_number)


def generate_otp(length: int = None) -> str:
    """
    Generate random OTP code
    
    Args:
        length: Length of OTP (default from settings)
    
    Returns:
        str: Random OTP code
    """
    if length is None:
        length = int(config('OTP_LENGTH', 6))
    return ''.join(random.choices(string.digits, k=length))


def validate_otp(otp_obj, entered_otp: str) -> tuple[bool, str]:
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
