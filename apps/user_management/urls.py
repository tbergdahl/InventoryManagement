from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_user, name="login_user"),
    path("index/", views.index, name="index"),
    path("logout/", views.logout_view, name="logout"),
]