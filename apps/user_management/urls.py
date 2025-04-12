from django.urls import path
from django.contrib.auth import views as auth_views
from apps.inventory.views import inventory_main_page
from . import views

urlpatterns = [
    # Login & Auth Flow
    path("", views.login_user, name="login_user"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("index/", views.direct_based_off_user, name="direct_to_page"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboards
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("admin_dash/", views.admin_dashboard, name="admin_dashboard"),
    path("admin_dash/manage_users/", views.manage_users, name="manage_users"),

    # Inventory
    path("inventory/", inventory_main_page, name="inventory_page"),

    # Password Reset Flow using reset_password/ templates
    path("password_reset/", 
         auth_views.PasswordResetView.as_view(template_name="reset_password/password_reset.html"), 
         name="password_reset"),

    path("password_reset/done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="reset_password/password_reset_done.html"), 
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="reset_password/password_reset_confirm.html"), 
         name="password_reset_confirm"),

    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="reset_password/password_reset_complete.html"), 
         name="password_reset_complete"),
]
