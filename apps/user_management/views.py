from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.http import HttpResponse
from .forms import CreateUserForm


def login_user(request):
    if request.method == "POST":
        print("Validating user")
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("direct_to_page") 
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
    return render(request, "admin_dashboard.html")

@login_required
def manage_users(request):
    users = CustomUser.objects.all()  # Get all users
    if request.method == 'POST':
        if 'delete_user' in request.POST:
            user_id = request.POST.get('delete_user')
            user = get_object_or_404(CustomUser, id=user_id)
            user.delete()
            return redirect('manage_users')  # Redirect to refresh the page after deletion
        elif 'create_user' in request.POST:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_users')  # Redirect to refresh the page after creation
    else:
        form = CreateUserForm()
    filtered_users = list(filter(lambda user: not user.isAdmin(), users))
    print(filtered_users)
    return render(request, 'manage_users.html', {'users': filtered_users, 'form': form})

def logout_view(request):
    logout(request)
    return redirect("login_user")  # Redirect back to login page after logout
