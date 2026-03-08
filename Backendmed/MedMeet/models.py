from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Contactform_DB(models.Model):
    name_enquiry = models.CharField(max_length=100,null=True,blank=True)
    email_enquiry = models.CharField(max_length=100,null=True,blank=True)
    phone_enquiry = models.CharField(max_length=100,null=True,blank=True)
    sub_enquiry = models.CharField(max_length=100,null=True,blank=True)
    message_enquiry = models.CharField(max_length=100,null=True,blank=True)

class SignUpDb(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    email=models.CharField(max_length=100,null=True,blank=True)
    password=models.CharField(max_length=100,null=True,blank=True)

class appointment(models.Model):
    customer_Country=models.CharField(max_length=100,null=True,blank=True)
    customer_Hospital=models.CharField(max_length=100,null=True,blank=True)
    customer_Department=models.CharField(max_length=100,null=True,blank=True)
    customer_Doctor=models.CharField(max_length=100,null=True,blank=True)
    customer_name=models.CharField(max_length=100,null=True,blank=True)
    customer_email=models.CharField(max_length=100,null=True,blank=True)
    customer_date=models.DateTimeField(null=True,blank=True)
    customer_message=models.CharField(max_length=100,null=True,blank=True)

class PatientProfile(models.Model):
    email=models.EmailField(unique=True, null=True, blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=15,null=True,blank=True)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.email} - {self.name}"

class OTP(models.Model):
    email=models.EmailField(null=True,blank=True)
    otp_code=models.CharField(max_length=6)
    is_used=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField()
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"OTP for {self.email}"
