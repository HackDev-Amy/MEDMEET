from django.contrib import admin
from medapp.models import Doctor_DB,Department_DB,Pharmacy_DB,Blog_DB,hospital_DB,appoint_DB
# Register your models here.

admin.site.register(Doctor_DB)
admin.site.register(Department_DB)
admin.site.register(Pharmacy_DB)
admin.site.register(Blog_DB)
admin.site.register(hospital_DB)
admin.site.register(appoint_DB)