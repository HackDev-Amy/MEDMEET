from django.db import models

# Create your models here.
class Doctor_DB(models.Model):
    D_hospital = models.CharField(max_length=100,null=True,blank=True)
    D_department = models.CharField(max_length=100,null=True,blank=True)
    D_name = models.CharField(max_length=100,null=True,blank=True)
    D_phone = models.CharField(max_length=100,null=True,blank=True)
    D_email = models.CharField(max_length=100,null=True,blank=True)
    D_image  = models.ImageField(upload_to='doctor photo',null=True,blank=True)
    D_age = models.CharField(max_length=100,null=True,blank=True)
    D_gender = models.CharField(max_length=100,null=True,blank=True)
    D_country = models.CharField(max_length=100,null=True,blank=True)
    D_bio = models.TextField(max_length=300,null=True,blank=True)
    D_contract = models.BooleanField(null=True,default=False)
    

class appoint_DB(models.Model):
    Acountry = models.CharField(max_length=100,null=True,blank=True)
    Ahospital = models.CharField(max_length=100,null=True,blank=True)
    Adepartment = models.CharField(max_length=100,null=True,blank=True)
    Adoctor = models.CharField(max_length=100,null=True,blank=True)
    AppointmentNO = models.IntegerField(null=True,blank=True)
    Aname = models.CharField(max_length=100,null=True,blank=True)
    Aphone = models.CharField(max_length=100,null=True,blank=True)
    Agender = models.CharField(max_length=100,null=True,blank=True)
    Ablood = models.CharField(max_length=100,null=True,blank=True)
    Adiabeties = models.CharField(max_length=100,null=True,blank=True)
    Atime = models.DateTimeField(null=True, blank=True)

class hospital_DB(models.Model):
    HosName = models.CharField(max_length=100,null=True,blank=True)
    HosDept1 = models.CharField(max_length=100,null=True,blank=True)
    HosDept2 = models.CharField(max_length=100,null=True,blank=True)
    HosDept3 = models.CharField(max_length=100,null=True,blank=True)
    HosDept4 = models.CharField(max_length=100,null=True,blank=True)
    HosDept5 = models.CharField(max_length=100,null=True,blank=True)
    HosDept6 = models.CharField(max_length=100,null=True,blank=True)
    HosEmail = models.CharField(max_length=100,null=True,blank=True)
    HosWebsite = models.CharField(max_length=100,null=True,blank=True)
    HosCountry = models.CharField(max_length=100,null=True,blank=True)
    HosNumber = models.CharField(max_length=100,null=True,blank=True)

class Department_DB(models.Model):
    DepName = models.CharField(max_length=100,null=True,blank=True)
    DepTime = models.CharField(max_length=100,null=True,blank=True)

class Country_DB(models.Model):
    CON_name = models.CharField(max_length=100,null=True,blank=True)
    CON_image  = models.ImageField(upload_to='Country photo',null=True,blank=True)
    

class Blog_DB(models.Model):
    Btitle = models.CharField(max_length=100,null=True,blank=True)
    Bimage = models.ImageField(upload_to='Blog Image',null=True,blank=True)
    Bcontent = models.TextField(max_length=300,null=True,blank=True)
    Bwriter = models.CharField(max_length=100,null=True,blank=True)

class Pharmacy_DB(models.Model):
    Medname = models.CharField(max_length=100,null=True,blank=True)
    Medimage = models.ImageField(upload_to='pharmacy image',null=True,blank=True)
    Medprice = models.CharField(max_length=100,null=True,blank=True)
    Medqty = models.CharField(max_length=100,null=True,blank=True)
    Medmanufacture = models.CharField(max_length=100,null=True,blank=True)
    Meduses = models.TextField(max_length=300,null=True,blank=True)
    Medside = models.TextField(max_length=300,null=True,blank=True)
    Meddesc = models.TextField(max_length=300,null=True,blank=True)
    