from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

    # Redirect base URL to the login page under accounts/
    path('', lambda request: redirect('/accounts/login/')),
]
