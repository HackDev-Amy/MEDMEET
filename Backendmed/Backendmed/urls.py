"""
URL configuration for Backendmed project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
import medapp.urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns,static
from . import settings
import MedMeet.urls

urlpatterns = [
    path('', lambda request: redirect('Med_Meet')),
    path('admin/', admin.site.urls),
    path('Backendmed/',include(medapp.urls)),
    path('frontendmed/',include(MedMeet.urls)),

]
urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
