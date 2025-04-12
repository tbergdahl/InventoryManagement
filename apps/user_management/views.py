from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.http import HttpResponse
from .forms import CreateUserForm
from django.core.mail import send_mail
from django.conf import settings
import random


def login_user(request):
    if request.method == "POST":
        print("Validating user")
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['pre_2fa_user'] = user.id

            # Generate 5-digit OTP
            otp = str(random.randint(10000, 99999))
            request.session['otp'] = otp

            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your verification code is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect("verify_otp")

        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        if entered_otp == request.session.get("otp"):
            user_id = request.session.get("pre_2fa_user")
            user = CustomUser.objects.get(id=user_id)
            login(request, user)
            del request.session['otp']
            del request.session['pre_2fa_user']
            return redirect("user_dashboard")
        else:
            return render(request, "verify_otp.html", {"error": "Invalid OTP"})

    return render(request, "verify_otp.html")


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
def user_dashboard(request):
    return render(request, "user_dashboard.html")


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
