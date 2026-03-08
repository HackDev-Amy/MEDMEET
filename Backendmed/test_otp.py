from django.test import Client

c = Client()
r = c.get('/frontendmed/otp_login/')
print(f'OTP Login page: {r.status_code}')
if r.templates:
    print(f'Template used: {r.templates[0].name}')
else:
    print('No template')
