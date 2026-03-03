from django.contrib.auth import authenticate, login
from django.shortcuts import redirect,render 
def staff_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.username == "hospital_a":
                return redirect("/hospital_a/")
            elif user.username == "hospital_b":
                return redirect("/hospital_b/")
            elif user.username == "hospital_c":
                return redirect("/hospital_c/")

        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")