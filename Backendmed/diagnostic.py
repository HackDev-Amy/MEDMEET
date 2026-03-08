#!/usr/bin/env python
"""
Diagnostic tool to identify issues in OTP system
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backendmed.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

print("=" * 80)
print("OTP SYSTEM DIAGNOSTIC TOOL")
print("=" * 80)

# Test 1: Environment Variables
print("\n1. CHECKING ENVIRONMENT CONFIGURATION...")
print("-" * 80)
try:
    from decouple import config
    sms_provider = config('SMS_PROVIDER', 'MOCK')
    print(f"   ✓ SMS Provider: {sms_provider}")
    
    otp_validity = config('OTP_VALIDITY_MINUTES', 10)
    print(f"   ✓ OTP Validity: {otp_validity} minutes")
    
    otp_length = config('OTP_LENGTH', 6)
    print(f"   ✓ OTP Length: {otp_length} digits")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Django Configuration
print("\n2. CHECKING DJANGO CONFIGURATION...")
print("-" * 80)
try:
    from django.conf import settings
    print(f"   ✓ Debug Mode: {settings.DEBUG}")
    print(f"   ✓ Database: {settings.DATABASES['default']['ENGINE']}")
    print(f"   ✓ Cache Backend: {settings.CACHES['default']['BACKEND']}")
    print(f"   ✓ Installed Apps: {len(settings.INSTALLED_APPS)} apps")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Database
print("\n3. CHECKING DATABASE...")
print("-" * 80)
try:
    from MedMeet.models import PatientProfile, OTP
    patients_count = PatientProfile.objects.count()
    otps_count = OTP.objects.count()
    print(f"   ✓ PatientProfile: {patients_count} records")
    print(f"   ✓ OTP: {otps_count} records")
    print(f"   ✓ Database connection: OK")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: OTP Service Module
print("\n4. CHECKING OTP SERVICE MODULE...")
print("-" * 80)
try:
    from MedMeet.otp_service import (
        generate_otp, 
        send_otp_sms, 
        validate_otp,
        get_sms_provider,
        send_otp_email
    )
    print(f"   ✓ generate_otp: OK")
    print(f"   ✓ send_otp_sms: OK")
    print(f"   ✓ validate_otp: OK")
    print(f"   ✓ get_sms_provider: OK")
    print(f"   ✓ send_otp_email: OK")
    
    provider = get_sms_provider()
    print(f"   ✓ SMS Provider loaded: {provider.__class__.__name__}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Views
print("\n5. CHECKING VIEWS...")
print("-" * 80)
try:
    from MedMeet.views import (
        otp_login,
        send_otp,
        verify_otp,
        patient_logout
    )
    print(f"   ✓ otp_login: OK")
    print(f"   ✓ send_otp: OK")
    print(f"   ✓ verify_otp: OK")
    print(f"   ✓ patient_logout: OK")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: URLs
print("\n6. CHECKING URL ROUTES...")
print("-" * 80)
try:
    from django.urls import resolve
    from django.test import Client
    
    client = Client()
    
    # Test URL resolution
    otp_login_match = resolve('/frontendmed/otp_login/')
    print(f"   ✓ /frontendmed/otp_login/ → {otp_login_match.view_name}")
    
    send_otp_match = resolve('/frontendmed/send_otp/')
    print(f"   ✓ /frontendmed/send_otp/ → {send_otp_match.view_name}")
    
    verify_otp_match = resolve('/frontendmed/verify_otp/')
    print(f"   ✓ /frontendmed/verify_otp/ → {verify_otp_match.view_name}")
    
    logout_match = resolve('/frontendmed/patient_logout/')
    print(f"   ✓ /frontendmed/patient_logout/ → {logout_match.view_name}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 7: Templates
print("\n7. CHECKING TEMPLATES...")
print("-" * 80)
try:
    from django.template.loader import get_template
    
    template = get_template('otp_login.html')
    print(f"   ✓ otp_login.html: Found and loadable")
    print(f"   ✓ Template size: {len(template.template.source)} bytes")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 8: Static & Media Files
print("\n8. CHECKING FILES...")
print("-" * 80)
try:
    otp_login_file = "MedMeet/templates/otp_login.html"
    otp_service_file = "MedMeet/otp_service.py"
    env_file = ".env"
    
    if os.path.exists(otp_login_file):
        print(f"   ✓ {otp_login_file}: Exists")
    else:
        print(f"   ✗ {otp_login_file}: Missing")
    
    if os.path.exists(otp_service_file):
        print(f"   ✓ {otp_service_file}: Exists")
    else:
        print(f"   ✗ {otp_service_file}: Missing")
    
    if os.path.exists(env_file):
        print(f"   ✓ {env_file}: Exists")
    else:
        print(f"   ⚠ {env_file}: Not found (will use defaults)")
    
    if os.path.exists("logs"):
        print(f"   ✓ logs/: Directory exists")
    else:
        print(f"   ⚠ logs/: Directory missing (will be created)")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 9: HTTP Requests
print("\n9. CHECKING HTTP ENDPOINTS...")
print("-" * 80)
try:
    client = Client()
    
    # Test OTP login page
    r = client.get('/frontendmed/otp_login/')
    print(f"   ✓ GET /frontendmed/otp_login/: {r.status_code}")
    
    if r.status_code == 200:
        if 'otp_login' in str(r.content).lower():
            print(f"     → Template rendered correctly")
    else:
        print(f"     ⚠ Unexpected status code")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 10: Logging
print("\n10. CHECKING LOGGING...")
print("-" * 80)
try:
    import logging
    logger = logging.getLogger('MedMeet.otp_service')
    
    if logger.handlers:
        print(f"   ✓ Logger configured: {len(logger.handlers)} handlers")
        for handler in logger.handlers:
            print(f"     → {handler.__class__.__name__}")
    else:
        print(f"   ⚠ No handlers configured")
        
    if os.path.exists("logs/medmeet.log"):
        print(f"   ✓ Log file: logs/medmeet.log")
    else:
        print(f"   ⚠ Log file not created yet")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)

print("\n✅ If all checks passed above, system is working correctly!")
print("\n⚠️  If you see any ✗ errors, note them and we can fix them.")
print("\nCommon Issues:")
print("  1. .env file missing → Create .env with SMS_PROVIDER=MOCK")
print("  2. Migrations not run → Run: python manage.py migrate")
print("  3. Static files not collected → Run: python manage.py collectstatic")
print("  4. File permissions → Run from venv with proper paths")

print("\nNext Steps:")
print("  1. Review diagnostic output above")
print("  2. Report any ✗ errors")
print("  3. Run: python test_otp_functional.py")
print("  4. Visit: http://localhost:8000/frontendmed/otp_login/")
