import random
import matplotlib
matplotlib.use("Agg")  # ✅ Use non-GUI backend for server

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .models import CustomUser
from .forms import CreateUserForm
from apps.inventory.models import InventoryRecord  # ✅ Added missing model

from django.utils.timezone import now
from datetime import datetime, timedelta  # ✅ Added timedelta
from django.db.models import Sum
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns


# ----------------------------
# Authentication Views
# ----------------------------

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pre_2fa_user'] = user.id
            otp = str(random.randint(10000, 99999))
            request.session['otp'] = otp
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


def logout_view(request):
    logout(request)
    return redirect("login_user")


# ----------------------------
# Dashboard Views
# ----------------------------

@login_required
def direct_based_off_user(request):
    if request.user.usertype == CustomUser.UType.ADMIN:
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
    users = CustomUser.objects.all()
    if request.method == 'POST':
        if 'delete_user' in request.POST:
            user = get_object_or_404(CustomUser, id=request.POST.get('delete_user'))
            user.delete()
            return redirect('manage_users')
        elif 'create_user' in request.POST:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_users')
    else:
        form = CreateUserForm()
    filtered_users = list(filter(lambda u: not u.isAdmin(), users))
    return render(request, 'manage_users.html', {'users': filtered_users, 'form': form})


# ----------------------------
# Product-wise Line Chart
# ----------------------------

@login_required
def product_line_chart(request):
    product = request.GET.get("product")
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)

    query = InventoryRecord.objects.filter(date_created__date__range=(start_date, end_date))
    if product:
        query = query.filter(product=product)

    data = query.values('date_created__date').annotate(sold=Sum('sold_quantity')).order_by('date_created__date')
    dates = [entry['date_created__date'].strftime('%Y-%m-%d') for entry in data]
    sold = [entry['sold'] for entry in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, sold, marker='o', linestyle='-', color='orange')
    plt.xticks(rotation=45)
    plt.title(f"Sales Report for {product}" if product else "Sales Report (All Products)")
    plt.xlabel("Date")
    plt.ylabel("Sold Quantity")
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')


# ----------------------------
# Product-wise Histogram
# ----------------------------

@login_required
def product_histogram(request):
    product = request.GET.get("product")
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)

    query = InventoryRecord.objects.filter(date_created__date__range=(start_date, end_date))
    if product:
        query = query.filter(product=product)

    sales = list(query.values_list('sales_rate', flat=True))
    if not sales:
        return HttpResponse("No sales data for this product.", content_type="text/plain")

    plt.figure(figsize=(10, 6))
    sns.histplot(sales, bins=12, kde=True, color='purple', edgecolor='black')
    plt.title(f"Sales Rate Distribution for {product}" if product else "All Products")
    plt.xlabel("Sales Rate")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')
