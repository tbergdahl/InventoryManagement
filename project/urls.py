"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def load_to_login(request):
    return redirect("login_user")

urlpatterns = [
    # Below redirects to user management app by default, which manages login
    path('', load_to_login),
    
    # loads admin app's urls
    path('admin/', admin.site.urls),
    
    # loads report gen app's urls
    path("report_generation/", include("apps.report_generation.urls")),
    
    # loads user management app's urls
    path("user_management/", include("apps.user_management.urls")),
    
    # loads inventory management app's urls
    path("inventory/", include("apps.inventory.urls")),
]
