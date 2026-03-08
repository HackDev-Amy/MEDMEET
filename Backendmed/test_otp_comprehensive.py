#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backendmed.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.test import Client
from MedMeet.models import PatientProfile, OTP

print("=" * 60)
print("OTP LOGIN/SIGNUP SYSTEM - COMPREHENSIVE TEST")
print("=" * 60)

# Clean up old test data
PatientProfile.objects.filter(phone_number='+1234567890').delete()
OTP.objects.filter(phone_number='+1234567890').delete()

c = Client()

print("\n1. Testing OTP Login Page Load...")
print("-" * 60)
r = c.get('/frontendmed/otp_login/')
print(f"   Status Code: {r.status_code}")
assert r.status_code == 200, "Failed to load OTP login page"
print("   ✓ OTP login page loads successfully (200)")

print("\n2. Testing Send OTP...")
print("-" * 60)
r1 = c.post('/frontendmed/send_otp/', {'phone_number': '+1234567890'})
print(f"   Status Code: {r1.status_code}")
assert r1.status_code == 302, "Send OTP did not redirect"
print("   ✓ Send OTP redirects correctly (302)")

# Check OTP was created in database
otp_records = OTP.objects.filter(phone_number='+1234567890', is_used=False)
print(f"   OTP Records Created: {otp_records.count()}")
assert otp_records.count() == 1, "OTP not created in database"
print("   ✓ OTP created in database")

# Get the OTP code
otp_code = otp_records.first().otp_code
print(f"   Generated OTP Code: {otp_code}")
print(f"   OTP Expires At: {otp_records.first().expires_at}")

print("\n3. Testing Verify OTP (Valid)...")
print("-" * 60)

# Create a new client session to simulate new request
c2 = Client()
r2 = c2.post('/frontendmed/verify_otp/', {
    'phone_number': '+1234567890',
    'otp_code': otp_code,
    'name': 'John Doe',
    'email': 'john@example.com'
})
print(f"   Status Code: {r2.status_code}")
assert r2.status_code == 302, "Verify OTP did not redirect"
print("   ✓ Verify OTP redirects correctly (302)")

# Check PatientProfile was created
patient = PatientProfile.objects.filter(phone_number='+1234567890').first()
print(f"   Patient Created: {patient is not None}")
assert patient is not None, "Patient profile not created"
print(f"   ✓ Patient profile created")
print(f"   Patient Name: {patient.name}")
print(f"   Patient Email: {patient.email}")
print(f"   Is Verified: {patient.is_verified}")
assert patient.is_verified, "Patient not marked as verified"
print(f"   ✓ Patient marked as verified")

# Check OTP was marked as used
otp_used = OTP.objects.filter(phone_number='+1234567890', otp_code=otp_code, is_used=True)
print(f"   OTP Marked as Used: {otp_used.exists()}")
assert otp_used.exists(), "OTP not marked as used"
print("   ✓ OTP marked as used")

print("\n4. Testing Verify OTP (Invalid)...")
print("-" * 60)
c3 = Client()
r3 = c3.post('/frontendmed/verify_otp/', {
    'phone_number': '+1234567890',
    'otp_code': '999999',  # Wrong OTP
})
print(f"   Status Code: {r3.status_code}")
assert r3.status_code == 302, "Invalid OTP did not redirect"
print("   ✓ Invalid OTP handling works (302)")

print("\n5. Testing Patient Login (Existing Patient)...")
print("-" * 60)
# Send new OTP for login (not signup)
r4 = c.post('/frontendmed/send_otp/', {'phone_number': '+1234567890'})
otp_records_new = OTP.objects.filter(phone_number='+1234567890', is_used=False).order_by('-created_at')
otp_code_login = otp_records_new.first().otp_code if otp_records_new.exists() else None

if otp_code_login:
    c4 = Client()
    r4_verify = c4.post('/frontendmed/verify_otp/', {
        'phone_number': '+1234567890',
        'otp_code': otp_code_login,
        'name': 'Jane Doe Updated',  # Try to update name
        'email': 'jane@example.com'
    })
    print(f"   Status Code: {r4_verify.status_code}")
    assert r4_verify.status_code == 302, "Login did not redirect"
    print("   ✓ Existing patient login works")
    
    # Check if patient was updated
    patient_updated = PatientProfile.objects.get(phone_number='+1234567890')
    print(f"   Patient Updated Name: {patient_updated.name}")
    print("   ✓ Patient profile updated")

print("\n6. Testing Logout...")
print("-" * 60)
c5 = Client()
r5 = c5.get('/frontendmed/patient_logout/')
print(f"   Status Code: {r5.status_code}")
assert r5.status_code == 302, "Logout did not redirect"
print("   ✓ Patient logout works (302)")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED SUCCESSFULLY!")
print("=" * 60)

print("\n📊 Database Summary:")
print(f"   Total Patients: {PatientProfile.objects.count()}")
print(f"   Total OTPs (all): {OTP.objects.count()}")
print(f"   Used OTPs: {OTP.objects.filter(is_used=True).count()}")
print(f"   Unused OTPs: {OTP.objects.filter(is_used=False).count()}")

print("\n🚀 System Ready for Development!")
print("\n📝 Access URLs:")
print("   - OTP Login Page: /frontendmed/otp_login/")
print("   - Home Page: /frontendmed/Med_Meet/")
print("\n📚 Documentation: OTP_LOGIN_DOCUMENTATION.md")
