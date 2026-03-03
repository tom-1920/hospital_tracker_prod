from django.shortcuts import render, redirect, get_object_or_404
from .models import HospitalStatus
from django.utils import timezone
import requests
from .utils import haversine
from hospital_a.models import Resource as ResourceA
from hospital_b.models import Resource as ResourceB
from hospital_c.models import Resource as ResourceC
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def dashboard(request):

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    radius = 10  # KM

    hospitals = HospitalStatus.objects.filter(available_beds__gt=0)
    hospitals=HospitalStatus.objects.all()
    query = request.GET.get("q") 
    if query:
        hospitals = hospitals.filter(hospital_name__icontains=query)

    if lat and lon:
        try:
            user_lat = float(lat)
            user_lon = float(lon)

            filtered = []

            for h in hospitals:
                if h.latitude and h.longitude:
                    dist = haversine(
                        user_lat, user_lon,
                        h.latitude, h.longitude
                    )

                    if dist <= radius:
                        h.distance = round(dist, 2)
                        filtered.append(h)

            hospitals = filtered

        except:
            pass

    return render(request, "central_tracker/dashboard.html", {
        "hospitals": hospitals
    })


def send_sos(request, hospital_id):
    hospital = get_object_or_404(HospitalStatus, id=hospital_id)

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    hospital.sos_active = True
    hospital.sos_time = timezone.now()

    if lat and lon:
        try:
            hospital.sos_latitude = float(lat)
            hospital.sos_longitude = float(lon)

            # Reverse Geocoding
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
            headers = {"User-Agent": "HealthGuardApp"}
            response = requests.get(url, headers=headers)
            data = response.json()

            hospital.sos_place = data.get("display_name", "Location unavailable")

        except:
            hospital.sos_place = "Location unavailable"
    else:
        hospital.sos_place = "Location not shared"

    hospital.save()
    messages.success(request, f"SOS sent successfully to {hospital.hospital_name}!")
    hospital_emails ={
        "HealthGuard Medical Center": "contact@healthguard-a.com",
        "CarePlus Hospital": "support@careplus-b.com",
        "LifeLine Medical Center": "info@lifeline-c.com",
    }
    recipient=hospital_emails.get(hospital.hospital_name)

    if recipient:
        send_mail(
            subject="MEDORM SOS Alert",
            message=f"An SOS alert has been triggered by {hospital.hospital_name} at {hospital.sos_time}. Location: {hospital.sos_place}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient],
        fail_silently=True,
    )
    return redirect("/")

def hospital_detail(request, hospital_id):
    hospital = get_object_or_404(HospitalStatus, id=hospital_id)

    resources = []

    if hospital.hospital_name == "HealthGuard Medical Center":
        resources = ResourceA.objects.using("hospital_a_db").all()

    elif hospital.hospital_name == "CarePlus Multispeciality Hospital":
        resources = ResourceB.objects.using("hospital_b_db").all()

    elif hospital.hospital_name == "Lifeline Advanced Medical Institute":
        resources = ResourceC.objects.using("hospital_c_db").all()

    return render(
        request,
        "central_tracker/hospital_detail.html",
        {
            "hospital": hospital,
            "resources": resources
        }
    )