"""
URL configuration for hospital_bed_medicine_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from .views import staff_login
from django.contrib.auth import logout
from django.shortcuts import redirect
def staff_logout(request):
    logout(request)
    return redirect("/login/")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('central_tracker.urls')),
    path('hospital_a/', include('hospital_a.urls')),
    path('hospital_b/', include('hospital_b.urls')),
    path('hospital_c/', include('hospital_c.urls')),
    path('login/', staff_login, name='staff_login'),
    path('logout/', staff_logout, name='staff_logout'),
]
