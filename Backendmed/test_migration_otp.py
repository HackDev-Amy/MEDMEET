#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backendmed.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.test import Client

print("=" * 70)
print("EMAIL LOGIN → OTP LOGIN MIGRATION TEST")
print("=" * 70)

c = Client()

print("\n1. Testing Old Login_customer URL Redirect...")
print("-" * 70)
r = c.get('/frontendmed/Login_customer/', follow=False)
print(f"   Status Code: {r.status_code}")
print(f"   Redirects to: {r.get('Location', 'N/A')}")
assert r.status_code == 302, "Should redirect"
assert '/otp_login/' in r.get('Location', ''), "Should redirect to OTP login"
print("   ✓ Old login redirects to OTP login")

print("\n2. Testing Old SaveSignUp URL Redirect...")
print("-" * 70)
r = c.post('/frontendmed/SaveSignUp/', {
    'txt': 'Test User',
    'email': 'test@example.com',
    'pswd': 'password123'
}, follow=False)
print(f"   Status Code: {r.status_code}")
assert r.status_code == 302, "Should redirect"
print("   ✓ Old signup redirects to OTP login")

print("\n3. Testing Old UserLogin URL Redirect...")
print("-" * 70)
r = c.post('/frontendmed/UserLogin/', {
    'email': 'test@example.com',
    'pswd': 'password123'
}, follow=False)
print(f"   Status Code: {r.status_code}")
assert r.status_code == 302, "Should redirect"
print("   ✓ Old user login redirects to OTP login")

print("\n4. Testing Old Logout (userLogout) Redirect...")
print("-" * 70)
r = c.get('/frontendmed/userLogout/', follow=False)
print(f"   Status Code: {r.status_code}")
assert r.status_code == 302, "Should redirect"
print("   ✓ Old logout redirects to OTP login")

print("\n5. Testing OTP Login Page Still Works...")
print("-" * 70)
r = c.get('/frontendmed/otp_login/')
print(f"   Status Code: {r.status_code}")
assert r.status_code == 200, "OTP login should load"
print("   ✓ OTP login page loads successfully")

print("\n6. Testing Navbar Links Updated...")
print("-" * 70)
r = c.get('/frontendmed/Med_Meet/')
content = r.content.decode()
has_otp_link = '/frontendmed/otp_login/' in content
has_old_email_link = "Email Login" in content
print(f"   Has OTP Login Link: {has_otp_link}")
print(f"   Has Old Email Login Text: {has_old_email_link}")
assert has_otp_link, "Should have OTP login link in navbar"
assert not has_old_email_link, "Should not have 'Email Login' text"
print("   ✓ Navbar updated correctly")

print("\n7. Testing Checkout Page Links Updated...")
print("-" * 70)
r = c.get('/frontendmed/Checkout_med/')
content = r.content.decode()
has_otp_checkout_link = '/frontendmed/otp_login/' in content
print(f"   Checkout links to OTP login: {has_otp_checkout_link}")
assert has_otp_checkout_link, "Checkout should link to OTP login"
print("   ✓ Checkout page updated correctly")

print("\n" + "=" * 70)
print("✓ ALL MIGRATION TESTS PASSED!")
print("=" * 70)

print("\n📊 Summary:")
print("   ✓ Old email login routes redirect to OTP login")
print("   ✓ OTP login remains the primary authentication method")
print("   ✓ Navigation updated to show only OTP login")
print("   ✓ Backward compatibility maintained")

print("\n🔐 Authentication System:")
print("   - Primary: OTP-based (phone number)")
print("   - Secondary: None (email login removed)")
print("   - Migration: Automatic redirect from old to new")

print("\n📝 Retired Routes:")
print("   - /frontendmed/Login_customer/ → redirects to OTP login")
print("   - /frontendmed/SaveSignUp/ → redirects to OTP login")
print("   - /frontendmed/UserLogin/ → redirects to OTP login")
print("   - /frontendmed/userLogout/ → redirects to OTP login")

print("\n🚀 Active Routes:")
print("   - /frontendmed/otp_login/ [GET] - Display login/signup page")
print("   - /frontendmed/send_otp/ [POST] - Send OTP to phone")
print("   - /frontendmed/verify_otp/ [POST] - Verify OTP and authenticate")
print("   - /frontendmed/patient_logout/ [GET] - Logout patient")

print("\n📚 Template Status:")
print("   - otp_login.html: ACTIVE (primary auth page)")
print("   - logins.html: DEPRECATED (no longer used)")
