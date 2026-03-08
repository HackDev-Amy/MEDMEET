from django.shortcuts import render, redirect
from medapp.models import appoint_DB,hospital_DB,Blog_DB,Doctor_DB,Department_DB,Pharmacy_DB,Country_DB
from MedMeet.models import Contactform_DB
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
from .forms import SuperuserForm


# ------------------image update error------------------------
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage


# ---------------------login for admin page---------------
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


import datetime

# --------------------javascripts alerts-------------------

from django.contrib import messages





# Create your views here.

# -------------------------mainpage-------------------------
def back_main(re):
    count1 = Doctor_DB.objects.count()
    count2 = hospital_DB.objects.count()
    count3 = Blog_DB.objects.count()
    count4 = Pharmacy_DB.objects.count()
    date = datetime.datetime.now()
    Customer_message=Contactform_DB.objects.all()
    return render(re,'index.html',{'count1':count1,'count2':count2,'count3':count3,'count4':count4,'date':date,'Customer_message':Customer_message})

# --------------------------------Doctor---------------------------

def add_doctor(re):
    hospital_data = hospital_DB.objects.all()
    data_department = Department_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'addDoc.html',{'hospital_data':hospital_data,'data_department':data_department,'date':date})

def save_doctor(re):
    if re.method=="POST":
        Doc_hospital = re.POST.get('Doc_Hospital')
        Doc_department = re.POST.get('Doc_Department')
        Doc_image = re.FILES['Doc_Image']
        Doc_name = re.POST.get('Doc_Name')
        Doc_email = re.POST.get('Doc_Email')
        Doc_phone = re.POST.get('Doc_Phone')
        Doc_age = re.POST.get('Doc_Age')
        Doc_gender = re.POST.get('Doc_Gender')
        Doc_country = re.POST.get('Doc_Country')
        Doc_bio = re.POST.get('Doc_Bio')
        Doc_contract = re.POST.get('D_contract')
        object=Doctor_DB(D_hospital=Doc_hospital,D_department=Doc_department,D_name=Doc_name,D_phone=Doc_phone,D_email=Doc_email,D_image=Doc_image,D_age=Doc_age,D_gender=Doc_gender,D_country=Doc_country,D_bio=Doc_bio,D_contract=Doc_contract)
        object.save()
        messages.success(re,'Doctor Profile Created....!')
        return redirect(add_doctor)
    
def display_doctor(re):
    doctor_data = Doctor_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'displaydoctor.html',{'doctor_data':doctor_data,'date':date})

def Doctor_edit(re,edit_id):
    data_edit = Doctor_DB.objects.get(id=edit_id)
    doctor_data = hospital_DB.objects.all()
    Departments_data = Department_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'Edit_doc.html',{'data_edit':data_edit,'doctor_data':doctor_data,'Departments_data':Departments_data,'date':date})

def gets_departments(request):
    hospital_name = request.POST.get('hospital_name')
    hospital = hospital_DB.objects.get(HosName=hospital_name)
    departments = [
        hospital.HosDept1,
        hospital.HosDept2,
        hospital.HosDept3,
        hospital.HosDept4,
        hospital.HosDept5,
        hospital.HosDept6,
    ]
    departments = [dept for dept in departments if dept]  # Remove empty departments
    return JsonResponse({'departments': departments})


def updatedoctor(re, update_id):
    if re.method=="POST":
        Doc_hospital = re.POST.get('Doc_Hospital')
        Doc_department = re.POST.get('Doc_Department')
        Doc_name = re.POST.get('Doc_Name')
        Doc_email = re.POST.get('Doc_Email')
        Doc_phone = re.POST.get('Doc_Phone')
        Doc_age = re.POST.get('Doc_Age')
        Doc_gender = re.POST.get('Doc_Gender')
        Doc_country = re.POST.get('Doc_Country')
        Doc_bio = re.POST.get('Doc_Bio')
        Doc_contract = re.POST.get('D_contract')

        try:
            image1 = re.FILES['Doc_Image']  # This is the input file field name
            fs = FileSystemStorage()
            C = fs.save(image1.name, image1)  # Save the image and get the filename

        except MultiValueDictKeyError:
            # If the image is not provided, get the existing image
            C = Doctor_DB.objects.get(id=update_id).D_image  # Use D_image here

        # Update the Doctor_DB instance with the new data
        Doctor_DB.objects.filter(id=update_id).update(
            D_hospital=Doc_hospital,
            D_department=Doc_department,
            D_name=Doc_name,
            D_phone=Doc_phone,
            D_email=Doc_email,
            D_image=C,  # Use D_image here
            D_age=Doc_age,
            D_gender=Doc_gender,
            D_country=Doc_country,
            D_bio=Doc_bio,
            D_contract=Doc_contract
        )

        messages.info(re,"Doctor Profile Updated.....")
        return redirect('display_doctor')  # Make sure 'display_doctor' is the correct URL name


def delete_doctor(re,del_id):
    Z=Doctor_DB.objects.get(id=del_id)
    Z.delete()
    messages.error(re,"Doctor Profile Deleted.....")
    return redirect(display_doctor)

# --------------------------------contact------------------------------------------------

def DeleteContact(re,D):
    x=Contactform_DB.objects.filter(id=D)
    x.delete()
    return redirect(back_main)

# -----------------------------------------------------------------------------------------------

# -------------------------------------appointment--------------------------------

def add_appointment(re):
    country_appoint = Country_DB.objects.all()
    hospital_appoint = hospital_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'addappointment.html',{'country_appoint':country_appoint,'hospital_appoint':hospital_appoint,'date':date})


def get_hospital_by_Country(request):   #_by_Country
    country_category = request.GET.get('country_category', '').strip()
    if country_category:
        # Filter hospitals by the selected country
        hospitals = hospital_DB.objects.filter(HosCountry__iexact=country_category).values('HosName')
        return JsonResponse(list(hospitals), safe=False)
    return JsonResponse([], safe=False)

def get_departments(request):      #_by_hospital
    hospital_name = request.GET.get('hospital_name', '').strip()
    if hospital_name:
        hospital = hospital_DB.objects.filter(HosName__iexact=hospital_name).first()
        if hospital:
            departments = [
                hospital.HosDept1, hospital.HosDept2, hospital.HosDept3,
                hospital.HosDept4, hospital.HosDept5, hospital.HosDept6
            ]
            # Remove empty departments
            departments = [dept.strip() for dept in departments if dept and dept.strip()]
            return JsonResponse({'departments': departments})
    return JsonResponse({'departments': []})


# def get_doctors(request):
#     hospital_name = request.GET.get('hospital_name', '')
#     department_name = request.GET.get('department_name', '')

#     if hospital_name and department_name:
#         try:
#             # Fetch doctors filtered by hospital and department
#             doctors = Doctor_DB.objects.filter(D_hospital=hospital_name, D_department=department_name).values('D_name', 'D_email', 'D_phone')
#             doctors_list = list(doctors)  # Convert QuerySet to a list of dictionaries
#             print(f"Filtered Doctors: {doctors_list}")  # Debugging log
#         except Exception as e:
#             print(f"Error fetching doctors: {e}")
#             doctors_list = []  # Fallback to empty list in case of an error
#     else:
#         print("Hospital name or department name is missing.")
#         doctors_list = []  # Return empty list if inputs are missing

#     return JsonResponse({'doctors': doctors_list})

def get_doctors(request):
    hospital_name = request.GET.get('hospital_name', '').strip()
    department_name = request.GET.get('department_name', '').strip()

    doctors_list = []
    if hospital_name:
        doctors_query = Doctor_DB.objects.filter(D_hospital__iexact=hospital_name)

        if department_name:
            department_matches = doctors_query.filter(D_department__iexact=department_name)
            if department_matches.exists():
                doctors_query = department_matches

        doctors_list = list(doctors_query.values('D_name', 'D_email', 'D_phone'))

    return JsonResponse({'doctors': doctors_list})


def save_appointment(re):
    if re.method=="POST":
      appoint_country=re.POST.get('country')
      appoint_hospital=re.POST.get('hospital')
      appoint_department=re.POST.get('department')
      appoint_doctor=re.POST.get('doctor')
      appoint_number=re.POST.get('appointnumber')
      patient_name=re.POST.get('patientname')
      mobile_number=re.POST.get('mobileno')
      gender=re.POST.get('gnederpatient')
      blood=re.POST.get('bloodgroup')
      diabeties_patient=re.POST.get('diabeties')
      book_time=re.POST.get('Time')
      object=appoint_DB(Acountry=appoint_country,Ahospital=appoint_hospital,Adepartment=appoint_department,Adoctor=appoint_doctor,AppointmentNO=appoint_number,Aname=patient_name,Aphone=mobile_number,Agender=gender,Ablood=blood,Adiabeties=diabeties_patient,Atime=book_time)
      object.save()
      messages.success(re,'Hospital Data Created....!')
      return redirect(add_appointment)
    
def delete_appoint(re,del_id):
    P=appoint_DB.objects.get(id=del_id)
    P.delete()
    messages.error(re,"Patient Data Deleted.....")
    return redirect(display_appointment)



def display_appointment(re):
    appoint_data=appoint_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'displayappoint.html',{'appoint_data':appoint_data,'date':date})

# -------------------------------hospital-----------------------------

def add_hosp(re):
    get_country = Country_DB.objects.all()
    get_department=Department_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'addhospital.html',{'get_country':get_country,'get_department':get_department,'date':date})

def save_hospital(re):
    if re.method=="POST":
      Hospital_name=re.POST.get('Hname')
      Hospital_website=re.POST.get('Hwebsite')
      Hospital_email=re.POST.get('Hemail')
      Hospital_Country=re.POST.get('Hcountry')
      Hospital_Number=re.POST.get('Hphone') 
      Hospital_Dept1=re.POST.get('Hdept1')
      Hospital_Dept2=re.POST.get('Hdept2')
      Hospital_Dept3=re.POST.get('Hdept3')
      Hospital_Dept4=re.POST.get('Hdept4')
      Hospital_Dept5=re.POST.get('Hdept5')
      Hospital_Dept6=re.POST.get('Hdept6')
      object=hospital_DB(HosName=Hospital_name, HosEmail=Hospital_email,HosWebsite=Hospital_website,HosCountry=Hospital_Country,HosNumber=Hospital_Number,HosDept1=Hospital_Dept1,HosDept2=Hospital_Dept2,HosDept3=Hospital_Dept3,HosDept4=Hospital_Dept4,HosDept5=Hospital_Dept5,HosDept6=Hospital_Dept6)
      object.save()
      messages.success(re,'Hospital Data Created....!')
      return redirect(add_hosp) 

def display_hospital(re):
    hospital_data = hospital_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'displayhosp.html',{'hospital_data':hospital_data,'date':date})

def delete_Hospital(re,del_id):
    Y=hospital_DB.objects.get(id=del_id)
    Y.delete()
    messages.error(re,"Hospital Data Deleted.....")
    return redirect(display_hospital)

# ------------------------------------------blog---------------------------------


def add_blog(re):
    date = datetime.datetime.now()
    return render(re,'addblog.html',{'date':date})

def display_blog(re):
    blog_data = Blog_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'displayblog.html',{'blog_data':blog_data,'date':date})

def save_blog(re):
    if re.method=="POST":
      BlogTitle=re.POST.get('Blogtitle')
      BlogImage=re.FILES['Blogimage']
      BlogContent=re.POST.get('Blogcontent')
      BlogWriter=re.POST.get('Blogwriter')
      object=Blog_DB(Btitle=BlogTitle,Bimage=BlogImage,Bcontent=BlogContent,Bwriter=BlogWriter)
      object.save()
      messages.success(re,'Blog Created....!')
      return redirect(add_blog)

def delete_blog(re,del_id):
    Z=Blog_DB.objects.get(id=del_id)
    Z.delete()
    messages.error(re,"Blog Deleted.....")
    return redirect(display_blog)

# --------------------------------------------countries---------------------------------------
def add_country(re):
    date = datetime.datetime.now()
    return render(re,'addcountry.html',{'date':date})

def display_country(re):
    country_data = Country_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'displaycountry.html',{'country_data':country_data,'date':date})

def save_country(re):
    if re.method=="POST":
        con_name=re.POST.get('Conname')
        con_image=re.FILES['Con_Image']
        object=Country_DB(CON_name=con_name,CON_image=con_image)
        object.save()
        messages.success(re,'New Country Added....!')
        return redirect(add_country)



def delete_country(re,del_id):
    C=Country_DB.objects.get(id=del_id)
    C.delete()
    messages.error(re,"Country Deleted.....")
    return redirect(display_country)
# ---------------------------------------------department--------------------------------



def add_department(re):
    date = datetime.datetime.now()
    return render(re,'adddepartment.html',{'date':date})


def save_Department(re):
    if re.method=="POST":
      Department_name=re.POST.get('Depname')
      Department_time=re.POST.get('Deptime') 
      object=Department_DB(DepName=Department_name, DepTime=Department_time)
      object.save()
      messages.success(re,'New Department Added....!')
      return redirect(add_department) 

def display_department(re):
    Department_data = Department_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'displaydepartment.html',{'Department_data':Department_data,'date':date})

def delete_department(re,del_id):
    D=Department_DB.objects.get(id=del_id)
    D.delete()
    messages.error(re,"Department Deleted.....")
    return redirect(display_department)

# ---------------------------Pharmacy-------------------------

def add_medicine(re):
    date = datetime.datetime.now()
    return render(re,'addpharmacy.html',{'date':date})

def save_medicine(re):
    if re.method=="POST":
      MedName=re.POST.get('Mname')
      MedImage=re.FILES['Mimage']
      MedPrice=re.POST.get('Mprice')
      MedQty=re.POST.get('Mqty')
      MedManu=re.POST.get('Manufac')
      MedUses=re.POST.get('Muses')
      MedSide=re.POST.get('Mside')
      MedDesc=re.POST.get('Mdesc')
      object=Pharmacy_DB(Medname=MedName,Medimage=MedImage,Medprice=MedPrice,Medqty=MedQty,Medmanufacture=MedManu,Meduses=MedUses,Medside=MedSide,Meddesc=MedDesc)
      object.save()
      messages.success(re,'New Medicine Added....!')
      return redirect(add_medicine)


def display_medicine(re):
    Pharmacy_data = Pharmacy_DB.objects.all()
    date = datetime.datetime.now()
    return render(re,'displaypharmacy.html',{'Pharmacy_data':Pharmacy_data,'date':date})

def delete_pharmacy(re,del_id):
    P=Pharmacy_DB.objects.get(id=del_id)
    P.delete()
    messages.error(re,"Medicine Deleted.....")
    return redirect(display_medicine)

# -------------------------admin----------------------

def aadmin_Login(re):
    return render(re,'admin_login.html')

def admin_login2(request):
    if request.method=='POST':
        user = request.POST.get('username')
        passwd = request.POST.get('pass')
        if User.objects.filter(username__contains=user).exists():
            user1 = authenticate(username=user, password=passwd)
            if user1 is not None:
                login(request, user1)
                # ------------------------login/logout session------------------
                request.session['username'] = user  
                request.session['password'] = passwd

                # -----------------------------------------------------------
                messages.success(request,'Welcome Admin...!')
                return redirect(back_main)
            else:
                messages.error(request,'Please Check your Password...!')
                return redirect(aadmin_Login)
        else:
            messages.warning(request,'Invalid Username...!')
            return redirect(aadmin_Login)

# def admin_logout(request):
#     del request.session['username']
#     del request.session['password']
#     messages.error(request,'Bye Admin...!')
#     return redirect(aadmin_Login)
def admin_logout(request):
    logout(request)
    request.session.flush()  # Clear the session data
    messages.success(request, 'Bye Admin...!')
    return redirect('aadmin_Login')

# ---------------------------------superuser--------------------------------------


def index(request):
    if request.method == 'POST':
        form = SuperuserForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if passwords match
            if password == confirm_password:
                # Check if username or email already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                else:
                    # Create a new superuser
                    user = User.objects.create_user(username, email, password)
                    user.is_superuser = True
                    user.is_staff = True  # Assuming you're creating an admin-level user
                    user.save()
                    messages.success(request, 'Superuser added successfully')
            else:
                messages.error(request, 'Passwords do not match')
        else:
            messages.error(request, 'Form is invalid')
    
    else:
        form = SuperuserForm()

    return render(request, 'index.html', {'form': form})

def my_view(request):
    host = request.get_host()
    port = request.get_port()
    url = f"http://{host}:{port}/admin/"
    return render(request, 'index.html', {'url': url})