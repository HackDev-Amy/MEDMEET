#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backendmed.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.test import Client

c = Client()

# Test OTP login page
print("Testing OTP Login Page...")
r = c.get('/frontendmed/otp_login/')
print(f'Status Code: {r.status_code}')
if r.templates:
    print(f'Template: {r.templates[0].name}')
    print("✓ OTP Login page loads successfully!")
else:
    print("Note: No template in response")

# Test sending OTP
print("\nTesting Send OTP...")
r2 = c.post('/frontendmed/send_otp/', {'phone_number': '+1234567890'})
print(f'Status Code: {r2.status_code}')

# Test verify OTP
print("\nTesting Verify OTP...")
r3 = c.post('/frontendmed/verify_otp/', {
    'phone_number': '+1234567890',
    'otp_code': '123456',
    'name': 'Test Patient',
    'email': 'test@example.com'
})
print(f'Status Code: {r3.status_code}')

print("\n✓ All tests completed!")
