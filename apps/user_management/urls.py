from django.urls import path
from apps.inventory.views import inventory_main_page
from . import views

urlpatterns = [
    path("", views.login_user, name="login_user"),
    path("index/", views.direct_based_off_user, name="direct_to_page"),
    path("logout/", views.logout_view, name="logout"),
    path("inventory/", inventory_main_page, name="inventory_page"),
    path("admin_dash/", views.admin_dashboard, name="admin_dashboard"),
    path("admin_dash/manage_users", views.manage_users, name="manage_users"),
    path("two_factor/", views.two_factor, name="two_factor"),
]