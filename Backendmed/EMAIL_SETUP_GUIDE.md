# 📧 Email OTP Setup Guide

## Setup Real Email Sending (FREE with Gmail)

Your OTP system is configured to send real emails via Gmail SMTP. Follow these steps:

### Step 1: Create/Use Gmail Account

1. Use an existing Gmail account or create a new one
2. Recommended: Create a dedicated account like `yourapp.noreply@gmail.com`

### Step 2: Enable 2-Factor Authentication

1. Go to: https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow steps to enable it

### Step 3: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer" (or Other)
3. Click "Generate"
4. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### Step 4: Update .env File

Edit `.env` file and update:

```env
EMAIL_HOST_USER=yourapp.noreply@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```

**Note:** Remove spaces from the app password!

### Step 5: Restart Django Server

```bash
python manage.py runserver
```

## ✅ Test Your Setup

1. Visit: http://localhost:8000/frontendmed/otp_login/
2. Enter your email
3. Click "Send OTP"
4. Check your email inbox for the OTP code
5. Enter the code and verify

## 🚀 Now Fully Functional!

- ✅ Single-page login (no tabs)
- ✅ Real email sending via Gmail
- ✅ Beautiful HTML email template
- ✅ 10-minute OTP expiry with timer
- ✅ Rate limiting (3 attempts per hour)
- ✅ Session-based authentication
- ✅ No test/console output

## Alternative: Use Console Mode (Testing Only)

If you want to test without real emails, change in `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

OTP codes will appear in the server console instead of email.

## Troubleshooting

### "Username and Password not accepted"
- Ensure 2FA is enabled
- Use App Password, not regular Gmail password
- Remove spaces from app password

### "SMTPAuthenticationError"
- Check EMAIL_HOST_USER is correct
- Verify App Password is correct
- Ensure 2FA is enabled

### Emails not arriving
- Check spam/junk folder
- Wait 1-2 minutes (Gmail may have delays)
- Try with a different email address

## Production Deployment

For production, consider:
- **SendGrid** - Free tier: 100 emails/day
- **Mailgun** - Free tier: 5,000 emails/month
- **AWS SES** - Very cheap, highly reliable

Contact me if you need help setting up production email!
