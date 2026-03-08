from django.urls import path
from MedMeet import views

urlpatterns = [
    path('Med_Meet/',views.Med_Meet, name='Med_Meet'),
    path('About_med/',views.About_med, name='About_med'),
    path('Blog_med/',views.Blog_med, name='Blog_med'),
    path('Blog1_med/<int:blogs1_id>/',views.Blog1_med, name='Blog1_med'),
    path('Hospital_med/',views.Hospital_med, name='Hospital_med'),
    path('Hospital_appointment/<int:hospital_id>/', views.Hospital_appointment, name='Hospital_appointment'),
    path('Contacts_med/',views.Contacts_med, name='Contacts_med'),
    path('SaveContact/',views.SaveContact, name='SaveContact'),
    path('Pharmacy_med/',views.Pharmacy_med, name='Pharmacy_med'),
    # path('pharmacy_search/',views.pharmacy_search, name='pharmacy_search'),
    path('Display_pharm/<int:single_id>/',views.Display_pharm, name='Display_pharm'),
    path('cart_med/',views.cart_med, name='cart_med'),
    path('Checkout_med/',views.Checkout_med, name='Checkout_med'),
    path('thank_med/',views.thank_med, name='thank_med'),
    path('Login_customer/',views.Login_customer, name='Login_customer'),
    path('SaveSignUp/',views.SaveSignUp, name='SaveSignUp'),
    path('UserLogin/',views.UserLogin, name='UserLogin'),
    path('userLogout/',views.userLogout, name='userLogout'),
    path('Saveappointments/',views.Saveappointments, name='Saveappointments'),
    path('otp_login/',views.otp_login, name='otp_login'),
    path('send_otp/',views.send_otp, name='send_otp'),
    path('verify_otp/',views.verify_otp, name='verify_otp'),
    path('patient_logout/',views.patient_logout, name='patient_logout'),
]