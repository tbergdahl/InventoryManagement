from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="data_gen_home"),
]