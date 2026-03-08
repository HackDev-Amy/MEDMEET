from django.urls import path
from medapp import views

urlpatterns = [
    path('back_main/',views.back_main, name='back_main'),

# ------------------------Doctor------------------------------
    path('add_doctor/',views.add_doctor, name='add_doctor'),
    path('save_doctor/',views.save_doctor, name='save_doctor'),
    path('display_doctor/',views.display_doctor, name='display_doctor'),
    path('Doctor_edit/<int:edit_id>/',views.Doctor_edit, name='Doctor_edit'),
    path('delete_doctor/<int:del_id>/',views.delete_doctor, name='delete_doctor'),
    path('updatedoctor/<int:update_id>/',views.updatedoctor, name='updatedoctor'),
    path('gets_departments/',views.gets_departments, name='gets_departments'),

    # --------------------------appointment------------------------------


    path('add_appointment/',views.add_appointment, name='add_appointment'),
    path('display_appointment/',views.display_appointment, name='display_appointment'),
    path('get_hospital_by_Country/',views.get_hospital_by_Country, name='get_hospital_by_Country'),
    path('get_departments/',views.get_departments, name='get_departments'),
    path('get_doctors/',views.get_doctors, name='get_doctors'),
    path('save_appointment/',views.save_appointment, name='save_appointment'),
    path('delete_appoint/<int:del_id>/',views.delete_appoint, name='delete_appoint'),



     # --------------------------Country------------------------------


    path('add_country/',views.add_country, name='add_country'),
    path('save_country/',views.save_country, name='save_country'),
    path('display_country/',views.display_country, name='display_country'),
    path('delete_country/<int:del_id>/',views.delete_country, name='delete_country'),


    # -----------------------hospital--------------------------------

    path('add_hosp/',views.add_hosp, name='add_hosp'),
    path('display_hospital/',views.display_hospital, name='display_hospital'),
    path('save_hospital/',views.save_hospital, name='save_hospital'),
    path('delete_Hospital/<int:del_id>/',views.delete_Hospital, name='delete_Hospital'),

    # ------------------------department-------------------------------

    path('add_department/',views.add_department, name='add_department'),
    path('save_Department/',views.save_Department, name='save_Department'),
    path('display_department/',views.display_department, name='display_department'),
    path('delete_department/<int:del_id>/',views.delete_department, name='delete_department'),

    # -----------------------------blog-------------------------------------

    path('add_blog/',views.add_blog, name='add_blog'),
    path('display_blog/',views.display_blog, name='display_blog'),
    path('save_blog/',views.save_blog, name='save_blog'),
    path('delete_blog/<int:del_id>/',views.delete_blog, name='delete_blog'),

# -------------------------------pharmacy--------------------------
    path('add_medicine/',views.add_medicine, name='add_medicine'),
    path('display_medicine/',views.display_medicine, name='display_medicine'),
    path('save_medicine/',views.save_medicine, name='save_medicine'),
    path('delete_pharmacy/<int:del_id>/',views.delete_pharmacy, name='delete_pharmacy'),

# ------------------------------admin---------------------------------

    path('aadmin_Login/',views.aadmin_Login, name='aadmin_Login'),
    path('admin_login2/',views.admin_login2, name='admin_login2'),
    path('admin_logout/',views.admin_logout, name='admin_logout'),

# --------------------------------------contact-------------------------------
    path('DeleteContact/<int:D>/',views.DeleteContact, name='DeleteContact'),

# ---------------------------------superuser-------------------------------------------
    path('index/',views.index, name='index'),
    path('my_view/', views.my_view, name='my_view'),
]