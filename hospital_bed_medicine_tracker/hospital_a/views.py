from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Resource
from central_tracker.models import HospitalStatus
from django.http import JsonResponse

HOSPITAL_NAME = "HealthGuard Medical Center"


@login_required
def update_availability(request):

    if request.user.username != "hospital_a":
        return redirect("/")

    hospital_status = HospitalStatus.objects.get(
        hospital_name=HOSPITAL_NAME
    )

    resources = Resource.objects.using("hospital_a_db").all()

    if request.method == "POST":

        # First update hospital DB values
        for resource in resources:
            field_name = f"resource_{resource.id}"
            value = request.POST.get(field_name)

            if value is not None:
                try:
                    resource.available_count = int(value)
                    resource.save(using="hospital_a_db")
                except ValueError:
                    pass

        # Refresh resources after update
        resources = Resource.objects.using("hospital_a_db").all()

        # Prepare sync values for central
        beds_total = 0
        icu = 0
        ventilator = 0
        rem = 0
        dex = 0
        oxy = 0

        for r in resources:
            if r.name == "General Beds":
                beds_total += r.available_count
            elif r.name == "ICU Beds":
                icu = r.available_count
            elif r.name == "Ventilator Beds":
                ventilator = r.available_count
            elif r.name == "Remdesivir":
                rem = r.available_count
            elif r.name == "Dexamethasone":
                dex = r.available_count
            elif r.name == "Oxygen Cylinders":
                oxy = r.available_count

        # Update central database
        HospitalStatus.objects.filter(
            hospital_name=HOSPITAL_NAME
        ).update(
            available_beds=beds_total,
            icu_beds=icu,
            ventilators=ventilator,
            remdesivir=rem,
            dexamethasone=dex,
            oxygen_cylinders=oxy
        )

        return redirect("hospital_a_update")

    sos = hospital_status.sos_active
    user_location = None

    if sos:
        user_location = f"{hospital_status.sos_latitude}, {hospital_status.sos_longitude}"

    return render(request, "hospital_a/update_availability.html", {
        "resources": resources,
        "sos": sos,
        "hospital_status": hospital_status
    })
@login_required
def clear_sos(request):
    HospitalStatus.objects.filter(
        hospital_name=HOSPITAL_NAME
    ).update(
        sos_active=False,
        sos_latitude=None,
        sos_longitude=None,
        sos_time=None
    )
def check_sos(request):
    hospital=HospitalStatus.objects.get(hospital_name="Hospital A")

    return JsonResponse({
        "sos_active":hospital.sos_active,
        "location":hospital.sos_place
    })


    return redirect("hospital_a_update")