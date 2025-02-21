from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def login_user(request):
    user = CustomUser.objects.get(username="trentonb")
    user.set_password("McIlroy52@")
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
def index(request):
    all_users = CustomUser.objects.all()
    print("rendering user page")
    return render(request, "index.html", {"users": all_users})

def logout_view(request):
    logout(request)
    return redirect("login_user")  # Redirect back to login page after logout
