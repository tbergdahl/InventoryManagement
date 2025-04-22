from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from .forms import InventoryItemForm, ThresholdForm
from .models import InventoryItem, ThresholdSetting, InventoryRecord
from django.utils.timezone import make_aware, now
from datetime import datetime, timedelta
import random
from django.urls import reverse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.db import models
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone




def is_admin(user):
    return user.is_authenticated and user.usertype == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def threshold_list(request):
    thresholds = ThresholdSetting.objects.all()
    return render(request, "threshold_list.html", {"thresholds": thresholds})

#Edit Modal
@login_required
@user_passes_test(is_admin)
def edit_threshold(request, pk):
    threshold = get_object_or_404(ThresholdSetting, pk=pk)

    if request.method == "POST":
        threshold.min_quantity = request.POST.get('min_quantity')
        threshold.max_quantity = request.POST.get('max_quantity')
        threshold.color = request.POST.get('color')
        threshold.template_message = request.POST.get('template_message')
        threshold.save()

        return redirect("threshold_list")

    return redirect("threshold_list")


# inventory/views.py

# delete Modal
@login_required
@user_passes_test(is_admin)
def delete_threshold(request, pk):
    threshold = get_object_or_404(ThresholdSetting, pk=pk)
    threshold.delete()
    return redirect('threshold_list')

# add Modal

@login_required
@user_passes_test(is_admin)
@require_POST
def add_threshold(request):
    product = request.POST.get("product")
    min_quantity = request.POST.get("min_quantity")
    max_quantity = request.POST.get("max_quantity")
    color = request.POST.get("color")
    template_message = request.POST.get("template_message")

    if product and min_quantity and max_quantity:
        ThresholdSetting.objects.create(
            product=product,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            color=color,
            template_message=template_message
        )

    return redirect("threshold_list")


# -----------------------------------
# Data Seeding View
# -----------------------------------

def load_test_data(request):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)
    days_range = (end_date - start_date).days

    vendors = ["Vendor A", "Vendor B", "Vendor C", "Vendor D"]
    categories = {
        "Perishable": ["Milk", "Eggs", "Yogurt", "Cheese", "Spinach", "Tomato", "Chicken", "Fish"],
        "Non-Perishable": ["Rice", "Pasta", "Canned Beans", "Soap", "Shampoo", "Notebook", "Chips", "Cereal"]
    }

    records = []

    for _ in range(200):
        category_type = random.choice(["Perishable", "Non-Perishable"])
        product = random.choice(categories[category_type])
        quantity = random.randint(20, 300)
        sold_quantity = random.randint(1, quantity)
        purchase_rate = round(random.uniform(5.0, 150.0), 2)
        sales_rate = round(purchase_rate + random.uniform(5.0, 60.0), 2)
        vendor = random.choice(vendors)
        rand_day_offset = random.randint(0, days_range)
        date_created = make_aware(start_date + timedelta(days=rand_day_offset))
        records.append(InventoryRecord(
            vendor=vendor,
            category=category_type,
            product=product,
            quantity=quantity,
            sold_quantity=sold_quantity,
            purchase_rate=purchase_rate,
            sales_rate=sales_rate,
            date_created=date_created
        ))

    for _ in range(20):
        category_type = random.choice(["Perishable", "Non-Perishable"])
        product = random.choice(categories[category_type])
        quantity = random.randint(20, 300)
        sold_quantity = random.randint(1, quantity)
        purchase_rate = round(random.uniform(5.0, 150.0), 2)
        sales_rate = round(purchase_rate + random.uniform(5.0, 60.0), 2)
        vendor = random.choice(vendors)
        date_created = make_aware(datetime.today() - timedelta(days=random.randint(0, 6)))
        records.append(InventoryRecord(
            vendor=vendor,
            category=category_type,
            product=product,
            quantity=quantity,
            sold_quantity=sold_quantity,
            purchase_rate=purchase_rate,
            sales_rate=sales_rate,
            date_created=date_created
        ))

    InventoryRecord.objects.bulk_create(records)
    return HttpResponse("220 test records inserted (200 general + 20 weekly).")


# -----------------------------------
# Date Filter Helper
# -----------------------------------
def get_date_filter(range_type):
    today = timezone.now().date()
    if range_type == "weekly":
        start = today - timedelta(days=7)
    elif range_type == "monthly":
        start = today - timedelta(days=90)
    else:
        start = today
    return {"recorded_at__date__range": (start, today)}

# -----------------------------------
# Chart Generators
# -----------------------------------
def generate_pie_chart(date_filter, label):
    data = InventoryRecord.objects.filter(**date_filter).values('product').annotate(total=models.Sum('quantity'))
    labels = [entry['product'] for entry in data]
    sizes = [entry['total'] for entry in data]
    plt.figure(figsize=(4.5, 4.5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f"{label} Pie Chart - Sales by Product")
    plt.axis('equal')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')

def generate_histogram(date_filter, label):
    sales = InventoryRecord.objects.filter(**date_filter).values_list('quantity', flat=True)
    plt.figure(figsize=(10, 6))
    sns.histplot(sales, bins=12, kde=True, color='green', edgecolor='black')
    plt.title(f"{label} Sales Rate Distribution")
    plt.xlabel("Sales Quantity")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')

def generate_line_chart(date_filter, label):
    data = InventoryRecord.objects.filter(**date_filter).values('recorded_at').annotate(
        sold=models.Sum('quantity')).order_by('recorded_at')
    dates = [entry['recorded_at'].strftime('%Y-%m-%d') for entry in data]
    sold = [entry['sold'] for entry in data]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, sold, marker='o', linestyle='-', color='blue')
    plt.xticks(rotation=45)
    plt.title(f"{label} Sales Report Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sold Quantity")
    plt.grid(True)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')

def generate_bar_chart(date_filter, label):
    data = InventoryRecord.objects.filter(**date_filter).values('product').annotate(sold=models.Sum('quantity'))
    categories = [entry['product'] for entry in data]
    sold = [entry['sold'] for entry in data]
    plt.figure(figsize=(6, 4))
    sns.barplot(x=categories, y=sold, palette="pastel")
    plt.title(f"{label} Product-wise Sales Report")
    plt.xlabel("Product")
    plt.ylabel("Sold Quantity")
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')

# -----------------------------------
# Weekly Chart Views
# -----------------------------------
def weekly_pie_chart(request): return generate_pie_chart(get_date_filter("weekly"), "Weekly")
def weekly_histogram(request): return generate_histogram(get_date_filter("weekly"), "Weekly")
def weekly_line_chart(request): return generate_line_chart(get_date_filter("weekly"), "Weekly")
def weekly_bar_chart(request): return generate_bar_chart(get_date_filter("weekly"), "Weekly")

# -----------------------------------
# Monthly Chart Views
# -----------------------------------
def monthly_pie_chart(request): return generate_pie_chart(get_date_filter("monthly"), "Monthly")
def monthly_histogram(request): return generate_histogram(get_date_filter("monthly"), "Monthly")
def monthly_line_chart(request): return generate_line_chart(get_date_filter("monthly"), "Monthly")
def monthly_bar_chart(request): return generate_bar_chart(get_date_filter("monthly"), "Monthly")

# -----------------------------------
# Product-wise Chart Views
# -----------------------------------
def product_line_chart(request):
    product = request.GET.get("product")
    start = request.GET.get("start")
    end = request.GET.get("end")
    date_filter = {}
    if start and end:
        date_filter["recorded_at__date__range"] = [start, end]
    if product:
        date_filter["product"] = product
    data = InventoryRecord.objects.filter(**date_filter).values('recorded_at').annotate(
        sold=models.Sum('quantity')).order_by('recorded_at')
    dates = [entry['recorded_at'].strftime('%Y-%m-%d') for entry in data]
    sold = [entry['sold'] for entry in data]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, sold, marker='o', linestyle='-', color='orange')
    plt.title(f"Sales Report for {product or 'All Products'}")
    plt.xlabel("Date")
    plt.ylabel("Sold Quantity")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')

def product_histogram(request):
    product = request.GET.get("product")
    start = request.GET.get("start")
    end = request.GET.get("end")
    date_filter = {}
    if start and end:
        date_filter["recorded_at__date__range"] = [start, end]
    if product:
        date_filter["product"] = product
    sales = InventoryRecord.objects.filter(**date_filter).values_list('quantity', flat=True)
    plt.figure(figsize=(10, 6))
    sns.histplot(sales, bins=12, kde=True, color='purple', edgecolor='black')
    plt.title(f"Sales Quantity Distribution for {product or 'All Products'}")
    plt.xlabel("Sales Quantity")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')

# Inventory Views

@login_required
def load_test_data(request):
    if request.user.usertype != 'ADMIN':
        return redirect('inventory_home')

    # Clear existing items
    InventoryItem.objects.all().delete()

    thresholds = ThresholdSetting.objects.all()

    for threshold in thresholds:
        if threshold.product:
            quantity = random.randint(threshold.min_quantity, threshold.max_quantity)
            expiry_date = timezone.now().date() + timedelta(days=random.randint(10, 60))

            InventoryItem.objects.create(
                name=threshold.product,                       
                category="Auto",                              # or use threshold.category if exists
                count=quantity,                              
                expiry_date=expiry_date,
                min_quantity=threshold.min_quantity,
                max_quantity=threshold.max_quantity,
                template_message=threshold.template_message
            )

    messages.success(request, "Test inventory data loaded successfully!")
    return redirect('inventory_home')

# Inventory home with filters and notifications

# Load Test Data from ThresholdSetting
@login_required
def load_test_data(request):
    if request.user.usertype != 'ADMIN':
        return redirect('inventory_home')

    # Clear existing inventory data
    InventoryItem.objects.all().delete()

    thresholds = ThresholdSetting.objects.all()

    for threshold in thresholds:
        if threshold.product:  # Make sure product is not None
            quantity = random.randint(threshold.min_quantity, threshold.max_quantity)
            expiry_date = timezone.now().date() + timedelta(days=random.randint(10, 60))

            InventoryItem.objects.create(
                name=threshold.product,         
                count=quantity,                 
               expiry_date=expiry_date,
               min_quantity=threshold.min_quantity,
               max_quantity=threshold.max_quantity,
              template_message=threshold.template_message
            )


    messages.success(request, "Test inventory data loaded successfully!")
    return redirect('inventory_home')


# Inventory Overview Page

@login_required
def inventory_home(request):
    inventory_items = InventoryItem.objects.all().order_by('-id')
    thresholds = ThresholdSetting.objects.all()

    threshold_lookup = {t.product.lower(): t for t in thresholds if t.product}
    notifications = []
    today = now().date()

    filter_expiry = request.GET.get("expiry", "")
    if filter_expiry == "this_month":
        inventory_items = [
            item for item in inventory_items
            if item.expiry_date and
               item.expiry_date.month == today.month and item.expiry_date.year == today.year
        ]

    combined_items = []
    for item in inventory_items:
        product_key = item.name.lower() if item.name else ""
        threshold = threshold_lookup.get(product_key)
        
        if threshold and item.count < threshold.min_quantity:
            msg = threshold.template_message.format(stock=item.count)
            notifications.append(f"⚠️ {item.name}: {msg}")

        if item.expiry_date and item.expiry_date < today:
            notifications.append(f"❗ {item.name} has expired on {item.expiry_date.strftime('%d %b %Y')}")

        #  replacement of {stock}
        if threshold and threshold.template_message and item.count is not None:
            message = threshold.template_message.replace("{stock}", str(item.count))
        else:
            message = "-"

        combined_items.append({
            "item": item,
            "threshold": threshold,
            "message": message
        })

    return render(request, 'inventory_home.html', {
        'combined_items': combined_items,
        'notifications': notifications,
        'is_admin': request.user.is_authenticated and request.user.usertype == 'ADMIN',
    })




#  Create new inventory item
@login_required
def create_inventory_item(request):
    if request.user.usertype != 'ADMIN':
        return redirect('inventory_home')

    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item created successfully!")
            return redirect('inventory_home')
    else:
        form = InventoryItemForm()

    return render(request, 'create_inventory_item.html', {'form': form})


#  Edit an inventory item
@login_required
def edit_item(request, item_id):
    if request.user.usertype != 'ADMIN':
        return redirect('inventory_home')

    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully!")
            return redirect('inventory_home')
    else:
        form = InventoryItemForm(instance=item)

    return render(request, 'edit_item.html', {'form': form, 'item': item})


#  Delete an inventory item
@login_required
def delete_item(request, item_id):
    if request.user.usertype != 'ADMIN':
        return redirect('inventory_home')

    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item deleted successfully!")
    return redirect('inventory_home')


# Edit Logic Item on Inventory


def edit_item(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)

    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.category = request.POST.get('category')
        item.count = request.POST.get('count')
        item.expiry_date = request.POST.get('expiry_date') or None
        item.min_quantity = request.POST.get('min_quantity') or None
        item.max_quantity = request.POST.get('max_quantity') or None
        item.template_message = request.POST.get('template_message')
        item.save()
        return redirect('inventory_home')

    # Load all items and thresholds again
    inventory_items = InventoryItem.objects.all().order_by('-id')
    thresholds = ThresholdSetting.objects.all()
    threshold_lookup = {t.product.lower(): t for t in thresholds}
    today = now().date()

    combined_items = []
    for i in inventory_items:
        threshold = threshold_lookup.get(i.name.lower())
        combined_items.append({'item': i, 'threshold': threshold})

    return render(request, 'inventory_home.html', {
        'combined_items': combined_items,
        'edit_item': item,
        'is_admin': True
    })
