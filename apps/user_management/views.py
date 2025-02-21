from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.http import HttpResponse
def login_user(request):
    user = CustomUser.objects.get(username="testemployee")
    user.set_password("dumbpassword1@")
    user.save()
    if request.method == "POST":
        print("Validating user")
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("index")  # Redirect to the user list page
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    
    return render(request, "login.html")

@login_required
def direct_based_off_user(request):
    current_user = request.user
    if current_user.usertype == CustomUser.UType.ADMIN:
        return redirect("admin_dashboard")
    else:
        return redirect("inventory_page")

@login_required
def admin_dashboard(request):
    return HttpResponse("Admin Dashboard")


def logout_view(request):
    logout(request)
    return redirect("login_user")  # Redirect back to login page after logout
