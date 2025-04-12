from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def load_to_login(request):
    return redirect("login_user")

urlpatterns = [
    # Redirect root URL to login
    path('', load_to_login),
    
    # Django admin panel
    path('admin/', admin.site.urls),
    
    # App-specific URL configs
    path("report_generation/", include("apps.report_generation.urls")),
    path("user_management/", include("apps.user_management.urls")),
    path("inventory/", include("apps.inventory.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
