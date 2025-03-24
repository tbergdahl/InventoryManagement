from django.urls import path
from .views import login_page, signup_page, verify_otp_page, welcome_page,logout_view


urlpatterns = [
    path("login/", login_page, name="login"),
    path("signup/", signup_page, name="signup"),
    path("verify-code/", verify_otp_page, name="verify-code"),
    path("welcome/", welcome_page, name="welcome"),
    path("Logout/", logout_view, name="logout" ),

]
