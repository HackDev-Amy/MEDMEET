# OTP Login/Signup System - Implementation Summary

## Overview
A unified OTP-based authentication system for patient login/signup. Two-column responsive design: left column for phone number entry, right column for OTP verification.

## Database Models

### PatientProfile
```python
- phone_number (CharField, unique): Patient's phone number
- name (CharField): Patient's full name
- email (CharField): Patient's email address
- is_verified (BooleanField): Verification status
- created_at (DateTimeField): Account creation timestamp
- updated_at (DateTimeField): Last update timestamp
```

### OTP
```python
- phone_number (CharField): Target phone number
- otp_code (CharField): 6-digit OTP code
- is_used (BooleanField): Whether OTP was already used
- created_at (DateTimeField): OTP generation time
- expires_at (DateTimeField): OTP expiration time (10 minutes)
- is_expired() method: Check if OTP has expired
```

## URL Routes

| Route | View | Purpose |
|-------|------|---------|
| `/frontendmed/otp_login/` | otp_login | Display unified login/signup page |
| `/frontendmed/send_otp/` | send_otp | Generate and send OTP to phone |
| `/frontendmed/verify_otp/` | verify_otp | Verify OTP and login/create patient |
| `/frontendmed/patient_logout/` | patient_logout | Logout patient |

## Views Workflow

### 1. otp_login(request)
- **Method**: GET
- **Returns**: Renders `otp_login.html` page
- **Session**: Checks for `otp_sent` flag to show OTP input column

### 2. send_otp(request)
- **Method**: POST
- **Input**: `phone_number` (form field)
- **Process**:
  1. Validates phone number (min 10 digits)
  2. Generates 6-digit random OTP
  3. Deletes old unexpired OTPs for this phone
  4. Creates new OTP valid for 10 minutes
  5. Stores phone in session (`temp_phone`)
  6. Sets session flag (`otp_sent = True`)
  7. **TODO**: Integrate SMS gateway (Twilio, AWS SNS, etc.)
- **Returns**: Redirect to `otp_login` page
- **Note**: For development, OTP is displayed in test mode

### 3. verify_otp(request)
- **Method**: POST
- **Input**: 
  - `phone_number` (hidden field)
  - `otp_code` (6-digit code)
  - `name` (optional)
  - `email` (optional)
- **Process**:
  1. Retrieves OTP record from database
  2. Checks if OTP exists, is valid, and not expired
  3. Marks OTP as used
  4. Gets or creates `PatientProfile`:
     - Creates new patient if phone doesn't exist
     - Updates existing patient if already registered
  5. Sets session variables:
     - `patient_id`: Patient database ID
     - `patient_phone`: Patient phone number
     - `patient_name`: Patient display name
  6. Clears temporary OTP session data
- **Returns**: Redirect to `Med_Meet` (home page) on success
- **Error Handling**: 
  - Invalid OTP → Error message, redirect to login
  - Expired OTP → Marks as used, shows error
  - Missing fields → Error message, redirect to login

### 4. patient_logout(request)
- **Method**: GET
- **Process**: Clears all patient-related session variables
- **Returns**: Redirect to `otp_login` page

## Template Features

### otp_login.html
- **Two-column layout** (responsive):
  - Left: Phone input form (gradient background)
  - Right: OTP verification form
  - Stacks on mobile (<768px)
  
- **Column 1 - Phone Entry**:
  - Phone input field with validation (pattern: +[0-9]{10,15})
  - Auto-formats with + prefix
  - Send OTP button
  - Info box about 10-min expiration
  
- **Column 2 - OTP Verification**:
  - Displays when OTP is sent
  - OTP input (6-digit, numeric only, auto-formatted)
  - Name input (optional)
  - Email input (optional)
  - Verify & Continue button
  - Countdown timer (10 minutes)
  - Resend OTP link
  - Change phone number button
  
- **Test Mode** (Development Only):
  - Displays actual OTP in yellow box: "TEST MODE - Your OTP: XXXXXX"
  - Remove in production by removing session storage of `otp_display`

- **Features**:
  - Real-time phone number formatting
  - 6-digit OTP input formatting
  - Automatic timer countdown
  - Disabled inputs/buttons during submission
  - Bootstrap alert messages
  - Auto-dismiss alerts (5 seconds)
  - Loading states with spinner icons
  - Responsive design with gradient styling

## Home Page Integration

The navigation bar now supports:
1. **OTP Login detection**: Checks `request.session.patient_phone`
2. **Dual login options**: OTP login + Email login
3. **Patient profile display**: Shows patient name and phone when logged in
4. **Logout functionality**: Links to both `patient_logout` and `userLogout`

## Session Variables

| Key | Type | Purpose |
|-----|------|---------|
| `patient_id` | int | Patient database ID |
| `patient_phone` | str | Authenticated patient phone |
| `patient_name` | str | Patient display name |
| `temp_phone` | str | Temporary phone for OTP process |
| `otp_sent` | bool | Flag indicating OTP was sent |
| `otp_display` | str | **DEV ONLY** - Test OTP display |

## SMS Integration (TODO)

To enable real SMS delivery, integrate with:
- **Twilio**: `from twilio.rest import Client`
- **AWS SNS**: `import boto3`
- **Firebase**: Firebase Cloud Messaging
- **Local SMS Provider**: Your regional SMS service

Replace the TODO comment in `send_otp()` view with actual SMS code:

```python
# Example with Twilio
from twilio.rest import Client

account_sid = 'YOUR_TWILIO_SID'
auth_token = 'YOUR_TWILIO_TOKEN'
client = Client(account_sid, auth_token)

message = client.messages.create(
    body=f'Your MedMeet OTP is: {otp_code}',
    from_='+1234567890',
    to=phone_number
)
```

## Testing

### Test Script: test_otp_full.py
```sh
python test_otp_full.py
```
- Tests OTP login page (HTTP 200)
- Tests send_otp endpoint (HTTP 302 redirect)
- Tests verify_otp endpoint (HTTP 302 redirect)
- Confirms PatientProfile creation

### Manual Testing
1. Navigate to: `/frontendmed/otp_login/`
2. Enter test phone: `+1234567890`
3. Click "Send OTP"
4. Copy 6-digit code from yellow test box
5. Enter name and email (optional)
6. Click "Verify & Continue"
7. Should redirect to home page
8. Navbar shows patient name and logout option

## Database Migration

Migrations created:
- `MedMeet/migrations/0010_otp_patientprofile.py`
  - Adds `OTP` model
  - Adds `PatientProfile` model

## Files Modified

1. **MedMeet/models.py**: Added `PatientProfile` and `OTP` models
2. **MedMeet/views.py**: Added OTP authentication views
3. **MedMeet/urls.py**: Added 4 OTP routes
4. **MedMeet/templates/otp_login.html**: New unified login page
5. **MedMeet/templates/Home.html**: Updated navbar with OTP support
6. **Database**: Applied migration 0010

## Security Considerations

- OTP valid for only 10 minutes
- Each OTP can only be used once
- Old OTPs are deleted before new one is created
- Phone number field is unique (one patient per phone)
- Passwords not used in OTP system (phone-based verification)
- Session variables cleared on logout
- Test OTP display should be removed in production

## Future Enhancements

1. Real SMS integration
2. OTP resend with cooldown (prevent abuse)
3. Demo number validation
4. Phone number update functionality
5. Account linking (merge OTP + email accounts)
6. Two-factor authentication (2FA)
7. Remember device option
8. Admin panel for OTP management
