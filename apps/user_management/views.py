from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import CreateUserForm
import random
from django.core.mail import send_mail
from django.conf import settings


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Generate a random 6-digit code
            two_factor_code = random.randint(100000, 999999)
            # Store the code and user id (as strings)
            request.session['two_factor_code'] = str(two_factor_code)
            request.session['two_factor_user_id'] = user.id
            
            # Send the code via gmail (settings.py)
            send_mail(
                subject='Your Two-Factor Authentication Code',
                message=f'Your authentication code is: {two_factor_code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            # Redirect to the two-factor authentication page.
            return redirect("two_factor")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    
    return render(request, "login.html")

def two_factor(request):
    if request.method == "POST":
        entered_code = request.POST.get("code")
        session_code = request.session.get("two_factor_code")
        user_id = request.session.get("two_factor_user_id")
        
        if entered_code == session_code and user_id:
            # Retrieve the user and log them in.
            user = CustomUser.objects.get(id=user_id)
            login(request, user)
            # Clean up the session
            del request.session["two_factor_code"]
            del request.session["two_factor_user_id"]
            return redirect("direct_to_page")
        else:
            return render(request, "two_factor.html", {"error": "Invalid code. Please try again."})
    
    return render(request, "two_factor.html")

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
