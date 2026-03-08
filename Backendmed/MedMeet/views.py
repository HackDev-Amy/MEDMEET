from django.shortcuts import render, redirect
from medapp.models import Doctor_DB,appoint_DB,hospital_DB,Department_DB,Blog_DB,Pharmacy_DB,Country_DB
from MedMeet.models import Contactform_DB,SignUpDb,appointment,PatientProfile,OTP
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from MedMeet.email_otp_service import send_otp_email, generate_otp, validate_otp
import random
import string





# Create your views here.
def Med_Meet(re):
    appointment_data = appointment.objects.all()
    email = re.session.get('email')
    country_appoint = Country_DB.objects.all()
    hospital_appoint = hospital_DB.objects.all()
    return render(re,'Home.html',{'country_appoint':country_appoint,'hospital_appoint':hospital_appoint,'email': email,'appointment_data':appointment_data})

def About_med(re):
    return render(re,'about.html')

def Blog_med(re):
    blog_profile=Blog_DB.objects.all()
    return render(re,'blogs.html',{'blog_profile':blog_profile})

def Blog1_med(re,blogs1_id):
    blog1_profile=Blog_DB.objects.get(id=blogs1_id)
    return render(re,'blogs1.html',{'blog1_profile':blog1_profile})

def Hospital_med(re):
    hospital_profile=hospital_DB.objects.all()
    return render(re,'hospitals.html',{'hospital_profile':hospital_profile})


def Hospital_appointment(re, hospital_id):
    selected_hospital = hospital_DB.objects.filter(id=hospital_id).first()
    if not selected_hospital:
        messages.error(re, "Selected hospital was not found.")
        return redirect(Hospital_med)

    departments = [
        selected_hospital.HosDept1,
        selected_hospital.HosDept2,
        selected_hospital.HosDept3,
        selected_hospital.HosDept4,
        selected_hospital.HosDept5,
        selected_hospital.HosDept6,
    ]
    departments = [department.strip() for department in departments if department and department.strip()]

    if re.method == "POST":
        appointment_department = re.POST.get('department')
        appointment_doctor = re.POST.get('doctor')
        appointment_name = re.POST.get('appoint_name')
        appointment_email = re.POST.get('appoint_email')
        appointment_date = re.POST.get('datetimes')
        appointment_message = re.POST.get('message')

        appointment_entry = appointment(
            customer_Country=selected_hospital.HosCountry,
            customer_Hospital=selected_hospital.HosName,
            customer_Department=appointment_department,
            customer_Doctor=appointment_doctor,
            customer_name=appointment_name,
            customer_email=appointment_email,
            customer_date=appointment_date,
            customer_message=appointment_message,
        )
        appointment_entry.save()
        messages.success(re, "Appointment request submitted successfully.")
        return redirect(Med_Meet)

    return render(
        re,
        'hospital_appointment.html',
        {
            'selected_hospital': selected_hospital,
            'departments': departments,
        },
    )


def Contacts_med(re):
    return render(re,'contacts.html')

def SaveContact(re):
    a=re.POST.get('Enquiry_name')
    b=re.POST.get('Enquiry_email')
    c=re.POST.get('Enquiry_subject')
    d=re.POST.get('Enquiry_Phone')
    e=re.POST.get('Enquiry_message')
    aa=Contactform_DB(name_enquiry=a,email_enquiry=b,sub_enquiry=c,phone_enquiry=d,message_enquiry=e)
    aa.save()
    return redirect(Contacts_med)

def Pharmacy_med(re):
    medicine_data=Pharmacy_DB.objects.all()
    return render(re,'Pharmacystore.html',{'medicine_data':medicine_data})

# def pharmacy_search(re):
#     if re.method == 'GET':
#         search = re.GET.get('search')
#         post = Pharmacy_DB.objects.all().filter(Medname=search)
#         return render(re,'searchpharmacy.html', {'post':post})

def Display_pharm(re,single_id):
    singlemed=Pharmacy_DB.objects.get(id=single_id)
    return render(re,'displaypharm.html',{'singlemed':singlemed})

def cart_med(re):
    return render(re,'cart.html')

def Checkout_med(re):
    country_data = Country_DB.objects.all()
    return render(re,'checkout.html', {'country_data':country_data})

def thank_med(re):
    return render(re,'thank.html')


def Login_customer(request):
    """Redirect old email login to OTP login"""
    messages.info(request, "Please use OTP-based login for enhanced security")
    return redirect('otp_login')


def SaveSignUp(re):
    """Old email signup - redirect to OTP signup"""
    messages.info(re, "Email signup is deprecated. Please use OTP-based signup")
    return redirect('otp_login')



def UserLogin(request):
    """Old email login - redirect to OTP login"""
    messages.info(request, "Email login is deprecated. Please use OTP-based authentication")
    return redirect('otp_login')



def userLogout(request):
    """Old email logout - redirect to OTP login"""
    request.session.pop('email', None)
    request.session.pop('password', None)
    messages.success(request, "Logged out successfully")
    return redirect('otp_login')


def Saveappointments(re):
    a2=re.POST.get('country')
    b2=re.POST.get('hospital')
    c2=re.POST.get('department')
    d2=re.POST.get('doctor')
    e2=re.POST.get('appoint_name')
    f2=re.POST.get('appoint_email')
    g2=re.POST.get('datetimes')
    h2=re.POST.get('message')
    bb=appointment(customer_Country=a2,customer_Hospital=b2,customer_Department=c2,customer_Doctor=d2,customer_name=e2,customer_email=f2,customer_date=g2,customer_message=h2)
    bb.save()
    return redirect(Med_Meet)


# ======================== OTP LOGIN/SIGNUP VIEWS ========================

def otp_login(request):
    """Display the unified email OTP login/signup page"""
    return render(request, 'email_otp_login.html')


def send_otp(request):
    """Generate and send OTP to email address (FREE!)"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        # Validate email
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not re.match(email_pattern, email):
            messages.error(request, "Please enter a valid email address")
            return redirect('otp_login')
        
        # Check rate limiting - max 3 OTP requests per email in 1 hour
        from django.core.cache import cache
        cache_key = f"otp_attempts_{email}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 3:
            messages.error(request, "Too many OTP requests. Please try again after 1 hour.")
            return redirect('otp_login')
        
        # Generate OTP
        otp_code = generate_otp()
        
        # Delete old unexpired OTPs for this email
        OTP.objects.filter(email=email, is_used=False).delete()
        
        # Create new OTP (valid for 10 minutes)
        otp_obj = OTP.objects.create(
            email=email,
            otp_code=otp_code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        
        # Send OTP via Email (FREE!)
        email_sent = send_otp_email(email, otp_code)
        
        if email_sent:
            # Increment rate limit counter
            cache.set(cache_key, attempts + 1, 3600)  # 1 hour expiry
            
            request.session['temp_email'] = email
            request.session['otp_sent'] = True
            messages.success(request, f"OTP sent to {email}")
        else:
            messages.info(request, f"OTP displayed in console (test mode)")
            request.session['temp_email'] = email
            request.session['otp_sent'] = True
        
        return redirect('otp_login')
    
    return redirect('otp_login')


def verify_otp(request):
    """Verify OTP and create/login patient"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        otp_code = request.POST.get('otp_code', '').strip()
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        if not email or not otp_code:
            messages.error(request, "Please enter email and OTP")
            return redirect('otp_login')
        
        # Check if OTP exists and is valid
        try:
            otp_obj = OTP.objects.filter(
                email=email,
                otp_code=otp_code,
                is_used=False
            ).latest('created_at')
            
            # Validate OTP
            is_valid, validation_message = validate_otp(otp_obj, otp_code)
            
            if not is_valid:
                messages.error(request, validation_message)
                return redirect('otp_login')
            
            # Mark OTP as used
            otp_obj.is_used = True
            otp_obj.save()
            
            # Check if patient exists, if not create new patient
            patient, created = PatientProfile.objects.get_or_create(
                email=email,
                defaults={
                    'is_verified': True,
                    'name': name,
                    'phone': phone
                }
            )
            
            if not created:
                # Update existing patient
                patient.is_verified = True
                if name:
                    patient.name = name
                if phone:
                    patient.phone = phone
                patient.save()
            
            # Set session
            request.session['patient_id'] = patient.id
            request.session['patient_email'] = patient.email
            request.session['patient_name'] = patient.name or patient.email
            
            messages.success(request, f"Welcome {patient.name or patient.email}! You are logged in.")
            return redirect('Med_Meet')
            
        except OTP.DoesNotExist:
            messages.error(request, "Invalid OTP or OTP not found. Please request a new OTP.")
            return redirect('otp_login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('otp_login')
    
    return redirect('otp_login')


def patient_logout(request):
    """Logout patient"""
    request.session.pop('patient_id', None)
    request.session.pop('patient_email', None)
    request.session.pop('patient_name', None)
    request.session.pop('temp_email', None)
    request.session.pop('otp_sent', None)
    messages.success(request, "Logged out successfully")
    return redirect('otp_login')