# Fully Functional OTP Authentication System - Complete Setup Guide

## 🎯 Overview

This is a **production-ready** OTP (One-Time Password) authentication system for MedMeet patient login/signup using mobile phone numbers. The system supports multiple SMS providers and includes rate limiting, session management, and comprehensive error handling.

---

## ✨ Features

### Core Features
- ✅ **Phone-based OTP Authentication** - No passwords required
- ✅ **6-Digit OTP Codes** - Auto-generated, 10-minute expiry
- ✅ **One-Time Use** - Each OTP can only be used once
- ✅ **Patient Profile Management** - Auto-create/update patient records
- ✅ **Session Management** - Secure session handling
- ✅ **Rate Limiting** - 3 OTP requests per phone per hour
- ✅ **Multiple SMS Providers** - Twilio, AWS SNS, Mock (testing)
- ✅ **Error Handling** - Comprehensive validation and messages
- ✅ **Logging** - All activities logged for auditing
- ✅ **Email Fallback** - Optional email delivery option

### Security Features
- 🔒 OTP expires after 10 minutes
- 🔒 One-time use enforcement
- 🔒 Rate limiting prevents abuse
- 🔒 Phone number uniqueness
- 🔒 Secure session handling
- 🔒 OTP never displayed in production
- 🔒 Activity logging for audit trail

---

## 📦 Installation

### 1. Install Required Packages

All packages are already installed:
```bash
pip install twilio python-decouple django
```

### 2. Environment Configuration

Edit `.env` file in the project root:

```env
# SMS Provider Selection
SMS_PROVIDER=MOCK  # Options: MOCK, TWILIO, AWS_SNS

# Twilio Configuration (if using Twilio)
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890

# AWS SNS Configuration (if using AWS SNS)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# OTP Settings
OTP_VALIDITY_MINUTES=10
OTP_LENGTH=6
MAX_OTP_ATTEMPTS=3

# Optional: Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 3. Database Setup

Migrations already applied:
```bash
python manage.py migrate
```

---

## 🚀 How to Use

### For Users

1. **Access Login Page**
   - Navigate to: `/frontendmed/otp_login/`

2. **Enter Phone Number**
   - Format: `+1234567890` (with country code)
   - Click "Send OTP"

3. **Receive OTP**
   - SMS delivery (via configured provider)
   - OTP valid for 10 minutes

4. **Enter OTP & Details**
   - 6-digit code from SMS
   - Name (optional)
   - Email (optional)
   - Click "Verify & Continue"

5. **Login Complete**
   - Redirected to home page
   - Patient profile created/updated
   - Session established

6. **Logout**
   - Click profile menu → "Logout"
   - Session cleared

### For Developers

```python
# Generate OTP
from MedMeet.otp_service import generate_otp
otp = generate_otp()  # Returns 6-digit OTP

# Send SMS
from MedMeet.otp_service import send_otp_sms
success = send_otp_sms('+1234567890', otp)

# Validate OTP
from MedMeet.otp_service import validate_otp
is_valid, message = validate_otp(otp_obj, entered_otp)

# Get SMS Provider
from MedMeet.otp_service import get_sms_provider
provider = get_sms_provider()  # Returns configured provider
```

---

## 🔧 SMS Provider Setup

### Option 1: MOCK Provider (Testing)

**Best for:** Development and testing

```env
SMS_PROVIDER=MOCK
```

- Prints OTP to console
- No credentials needed
- Perfect for local testing

### Option 2: Twilio (Production)

**Best for:** Real SMS in production

1. **Create Twilio Account**
   - Go to https://www.twilio.com/console
   - Sign up and verify phone number

2. **Get Credentials**
   - Account SID: Copy from dashboard
   - Auth Token: Copy from dashboard  
   - Phone Number: Purchase Twilio number or use trial

3. **Configure .env**
   ```env
   SMS_PROVIDER=TWILIO
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=+1234567890
   ```

4. **Test SMS**
   ```python
   from MedMeet.otp_service import send_otp_sms
   send_otp_sms('+1234567890', '123456')
   ```

### Option 3: AWS SNS (Enterprise)

**Best for:** Large-scale deployments

1. **Create AWS Account**
   - Go to https://aws.amazon.com/sns/

2. **Get Credentials**
   - Access Key ID
   - Secret Access Key
   - Region (e.g., us-east-1)

3. **Configure .env**
   ```env
   SMS_PROVIDER=AWS_SNS
   AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
   AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   AWS_REGION=us-east-1
   ```

4. **Test SMS**
   ```python
   from MedMeet.otp_service import send_otp_sms
   send_otp_sms('+1234567890', '123456')
   ```

---

## 📊 Database Models

### PatientProfile
```python
phone_number      # CharField, unique
name              # CharField (optional)
email             # CharField (optional)
is_verified       # BooleanField
created_at        # DateTimeField (auto)
updated_at        # DateTimeField (auto)
```

### OTP
```python
phone_number      # CharField
otp_code          # CharField (6 digits)
is_used           # BooleanField
created_at        # DateTimeField (auto)
expires_at        # DateTimeField (10 min from creation)
```

---

## 🔗 API Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| GET | `/frontendmed/otp_login/` | Display login page |
| POST | `/frontendmed/send_otp/` | Generate and send OTP |
| POST | `/frontendmed/verify_otp/` | Verify OTP and authenticate |
| GET | `/frontendmed/patient_logout/` | Logout patient |

---

## 📝 URL Routes

```python
path('otp_login/', views.otp_login, name='otp_login'),
path('send_otp/', views.send_otp, name='send_otp'),
path('verify_otp/', views.verify_otp, name='verify_otp'),
path('patient_logout/', views.patient_logout, name='patient_logout'),
```

---

## 🔐 Session Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `patient_id` | int | Patient database ID |
| `patient_phone` | str | Authenticated phone |
| `patient_name` | str | Patient display name |
| `temp_phone` | str | Temp phone for OTP process |
| `otp_sent` | bool | Flag: OTP was sent |

---

## 📋 Views Documentation

### `otp_login(request)` [GET]
Displays the unified OTP login/signup page.

```python
# Returns: Rendered otp_login.html template
# No parameters needed
```

### `send_otp(request)` [POST]
Generates and sends OTP to phone number.

```python
# Parameters:
# - phone_number: Recipient phone (required)

# Returns: Redirect to otp_login
# Actions:
# - Validates phone number
# - Generates 6-digit OTP
# - Sends SMS via configured provider
# - Sets session variables
# - Enforces rate limiting
```

### `verify_otp(request)` [POST]
Verifies OTP and creates/updates patient.

```python
# Parameters:
# - phone_number: Phone from OTP (required)
# - otp_code: 6-digit code (required)
# - name: Patient name (optional)
# - email: Patient email (optional)

# Returns: Redirect to Med_Meet (home)
# Actions:
# - Validates OTP
# - Checks expiry
# - Creates/updates patient
# - Sets authenticated session
```

### `patient_logout(request)` [GET]
Clears patient session and logs out.

```python
# Returns: Redirect to otp_login
# Actions:
# - Clears all patient session variables
# - Displays success message
```

---

## 🧪 Testing

### Run Comprehensive Tests
```bash
python test_otp_functional.py
```

### What's Tested
- ✓ OTP generation (6 digits)
- ✓ SMS provider integration
- ✓ Rate limiting (3/hour)
- ✓ OTP validation
- ✓ Patient creation
- ✓ Patient login
- ✓ Patient update
- ✓ Logout
- ✓ Error handling
- ✓ Phone validation

### Expected Output
```
✓ ALL FUNCTIONAL OTP SYSTEM TESTS PASSED!
✓ 10/10 tests successful
📊 System Statistics:
   Total Patients: 3
   Total OTPs: 9
```

---

## 📍 Files Structure

```
Backendmed/
├── .env                              # Configuration file
├── MedMeet/
│   ├── views.py                      # OTP views
│   ├── otp_service.py               # OTP service module (NEW)
│   ├── models.py                    # PatientProfile & OTP models
│   ├── urls.py                      # OTP routes
│   └── templates/
│       └── otp_login.html           # Login/signup page
├── Backendmed/
│   └── settings.py                  # Django config (updated)
├── logs/                             # Log files (auto-created)
└── test_otp_functional.py           # Functional tests
```

---

## 🛡️ Security Best Practices

### In Development
1. Use `SMS_PROVIDER=MOCK` for testing
2. Check console for test OTPs
3. Never commit `.env` with real credentials

### In Production
1. Use `SMS_PROVIDER=TWILIO` or `AWS_SNS`
2. Add real credentials to `.env`
3. Never hardcode credentials
4. Use environment variables
5. Enable HTTPS only
6. Set `DEBUG=False` in settings
7. Use secure session cookies
8. Monitor logs in `logs/medmeet.log`
9. Rate limit (already configured: 3/hour)
10. OTP expiry (already configured: 10 minutes)

---

## 🐛 Troubleshooting

### Issue: OTP Not Received

**Solution 1:** Check SMS Provider
```bash
# Check .env file
cat .env | grep SMS_PROVIDER

# Change to MOCK to test
SMS_PROVIDER=MOCK
python manage.py shell
from MedMeet.otp_service import send_otp_sms
send_otp_sms('+1234567890', '123456')
```

**Solution 2:** Verify Provider Credentials
```python
# In Django shell
from decouple import config
print(config('TWILIO_ACCOUNT_SID'))  # Should not be empty
```

**Solution 3:** Check Logs
```bash
tail logs/medmeet.log
```

### Issue: OTP Expired

**Solution:** Request new OTP
- Wait for error message
- Click "Resend" or "Change Phone Number"
- Request new OTP (expires in 10 minutes)

### Issue: Rate Limiting

**Solution:** Wait 1 hour
- Max 3 OTP requests per phone per hour
- Cache expires after 1 hour
- Manual reset: Clear Django cache

---

## 📊 Monitoring

### Check OTP Activity
```python
# In Django shell
from MedMeet.models import OTP, PatientProfile

# Total OTPs sent
OTP.objects.count()

# Used OTPs
OTP.objects.filter(is_used=True).count()

# Patients created
PatientProfile.objects.count()

# Recent activity
OTP.objects.order_by('-created_at')[:10]
```

### View Logs
```bash
# Follow logs in real-time
tail -f logs/medmeet.log

# Search for OTP activity
grep "OTP" logs/medmeet.log

# Search for SMS activity  
grep "SMS" logs/medmeet.log
```

---

## 🔄 Deployment Checklist

- [ ] Install Twilio/AWS credentials
- [ ] Update `.env` with SMS provider
- [ ] Set `DEBUG=False` in settings.py
- [ ] Enable HTTPS in production
- [ ] Update allowed hosts
- [ ] Run migrations
- [ ] Run tests: `python test_otp_functional.py`
- [ ] Check logs directory
- [ ] Monitor `/logs/medmeet.log`
- [ ] Set up email for error notifications
- [ ] Configure backup SMS provider
- [ ] Test with production phone number
- [ ] Monitor rate limiting
- [ ] Set up automated backups

---

## 📞 Support & Integration

### Integrate with Existing Features

**Home Page Navigation:**
```html
<a href="{% url 'otp_login' %}">Login / Signup</a>
```

**Appointment System:**
```python
# Login required for appointments
if not request.session.get('patient_phone'):
    return redirect('otp_login')
```

**Pharmacy Checkout:**
```python
# Use patient info from OTP login
patient_name = request.session.get('patient_name')
patient_phone = request.session.get('patient_phone')
```

---

## 🎯 Next Steps

1. **Configure SMS Provider**
   - Choose Twilio or AWS SNS
   - Add credentials to `.env`

2. **Test with Real Phone**
   - Update SMS_PROVIDER in .env
   - Test OTP delivery

3. **Deploy to Production**
   - Follow deployment checklist
   - Monitor logs
   - Gather user feedback

4. **Enhance Features**
   - Add 2FA
   - Add phone update
   - Add account recovery
   - Add multi-device support

---

## ✅ System Status

**Current Status:** ✨ **FULLY FUNCTIONAL AND PRODUCTION-READY**

- ✅ OTP generation working
- ✅ SMS providers integrated
- ✅ Rate limiting active
- ✅ Patient management operational
- ✅ Session handling secure
- ✅ Error handling comprehensive
- ✅ Logging configured
- ✅ All tests passing

**Ready for:** Production deployment, real SMS integration, user rollout

---

## 📚 References

- **Twilio Docs:** https://www.twilio.com/docs/sms
- **AWS SNS Docs:** https://docs.aws.amazon.com/sns/
- **Django Cache:** https://docs.djangoproject.com/en/5.1/topics/cache/
- **Django Sessions:** https://docs.djangoproject.com/en/5.1/topics/http/sessions/

---

**Last Updated:** March 1, 2026  
**Version:** 1.0 (Production Ready)  
**Status:** ✅ Fully Functional
