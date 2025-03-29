from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TwoFactorAuth
import random

# Login Page — Step 1: Authenticate and send OTP
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        method = "gmail"  # Default email method

        user = authenticate(username=username, password=password)
        if not user:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})

        otp = random.randint(10000, 99999)
        twofa, _ = TwoFactorAuth.objects.get_or_create(user=user)
        twofa.otp_code = otp
        twofa.otp_expires_at = now() + timedelta(minutes=10)  # 10-minute expiry
        twofa.email_method = method
        twofa.save()

        print("[DEBUG] OTP generated and saved:", otp)

        if user.email:
            send_otp_via_email(user.email, otp, method)
        else:
            return render(request, "accounts/login.html", {"error": "Email not found for this user."})

        return redirect(f"/accounts/verify-code/?username={username}")

    return render(request, "accounts/login.html")


# OTP Page — Step 2: Verify OTP
def verify_otp_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        otp = request.POST.get("otp")

        if not username or not otp:
            return render(request, "accounts/verify_otp.html", {
                "error": "OTP or username missing.",
                "username": username
            })

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "accounts/verify_otp.html", {
                "error": "User not found.",
                "username": username
            })

        try:
            twofa = TwoFactorAuth.objects.get(user=user)
        except TwoFactorAuth.DoesNotExist:
            return render(request, "accounts/verify_otp.html", {
                "error": "OTP not found. Request a new one.",
                "username": username
            })

        try:
            otp = int(otp)
        except ValueError:
            return render(request, "accounts/verify_otp.html", {
                "error": "OTP must be numeric.",
                "username": username
            })

        if twofa.otp_code == otp and now() < twofa.otp_expires_at:
            login(request, user)
            print("[DEBUG] OTP verified successfully.")
            return redirect("welcome")  # Redirect to welcome page after successful OTP

        print("[DEBUG] OTP mismatch or expired.")
        return render(request, "accounts/verify_otp.html", {
            "error": "Invalid or expired OTP.",
            "username": username
        })

    username = request.GET.get("username")
    return render(request, "accounts/verify_otp.html", {"username": username})


# Signup Page — Prevents duplicate username/email before inserting into DB
def signup_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        # Check for existing username or email
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {
                "error": "Username already exists."
            })

        if User.objects.filter(email=email).exists():
            return render(request, "accounts/signup.html", {
                "error": "Email already registered."
            })

        # Only save user if both are unique
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        TwoFactorAuth.objects.create(user=user)

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "accounts/signup.html")


# Welcome Page — Shown after successful 2FA login
def welcome_page(request):
    return render(request, "accounts/welcome.html")


# Logout Page
def logout_view(request):
    logout(request)
    return render(request, "accounts/logout.html")



# Send OTP via Email (Gmail or Outlook)
def send_otp_via_email(email, otp, method):
    sender = settings.EMAIL_HOST_USER if method == "gmail" else settings.OUTLOOK_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD if method == "gmail" else settings.OUTLOOK_HOST_PASSWORD

    print("[DEBUG] Sending OTP email to:", email)

    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is {otp}. It expires in 10 minutes.",
        from_email=sender,
        recipient_list=[email],
        auth_user=sender,
        auth_password=password,
        fail_silently=False
    )
