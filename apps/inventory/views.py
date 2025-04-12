from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from .forms import InventoryItemForm
from .models import PerishableInventoryItem, NonPerishableInventoryItem, InventoryItem, InventoryRecord
from django.utils.timezone import make_aware, now
from datetime import datetime, timedelta
import random

import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend

import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.db import models

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

    # Add 200 records from last 90 days
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

    #  Add 20 guaranteed records in the last 7 days
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


def get_date_filter(timeframe):
    today = now().date()
    
    if timeframe == "weekly":
        return {"date_created__date__gte": today - timedelta(days=7)}
    
    elif timeframe == "monthly":
        # Use LAST MONTH instead of current month for meaningful charts
        first_day_this_month = today.replace(day=1)
        last_month = first_day_this_month - timedelta(days=1)
        return {"date_created__year": last_month.year, "date_created__month": last_month.month}

    return {}


# -----------------------------------
# Chart Generators
# -----------------------------------
def generate_pie_chart(date_filter, label):
    data = InventoryRecord.objects.filter(**date_filter).values('category').annotate(total=models.Sum('sold_quantity'))
    labels = [entry['category'] for entry in data]
    sizes = [entry['total'] for entry in data]
    plt.figure(figsize=(4.5, 4.5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f"{label} Pie Chart - Sales by Category")
    plt.axis('equal')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')

def generate_histogram(date_filter, label):
    sales = InventoryRecord.objects.filter(**date_filter).values_list('sales_rate', flat=True)
    plt.figure(figsize=(10, 6))
    sns.histplot(sales, bins=12, kde=True, color='green', edgecolor='black')
    plt.title(f"{label} Sales Rate Distribution")
    plt.xlabel("Sales Rate")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')

def generate_line_chart(date_filter, label):
    data = InventoryRecord.objects.filter(**date_filter).values('date_created').annotate(sold=models.Sum('sold_quantity')).order_by('date_created')
    dates = [entry['date_created'].strftime('%Y-%m-%d') for entry in data]
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
    data = InventoryRecord.objects.filter(**date_filter).values('category').annotate(sold=models.Sum('sold_quantity'))
    categories = [entry['category'] for entry in data]
    sold = [entry['sold'] for entry in data]
    plt.figure(figsize=(6, 4))
    sns.barplot(x=categories, y=sold, palette="pastel")
    plt.title(f"{label} Category-wise Sales Report")
    plt.xlabel("Category")
    plt.ylabel("Sold Quantity")
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')

# Weekly Chart Views
def weekly_pie_chart(request): return generate_pie_chart(get_date_filter("weekly"), "Weekly")
def weekly_histogram(request): return generate_histogram(get_date_filter("weekly"), "Weekly")
def weekly_line_chart(request): return generate_line_chart(get_date_filter("weekly"), "Weekly")
def weekly_bar_chart(request): return generate_bar_chart(get_date_filter("weekly"), "Weekly")

# Monthly Chart Views
def monthly_pie_chart(request): return generate_pie_chart(get_date_filter("monthly"), "Monthly")
def monthly_histogram(request): return generate_histogram(get_date_filter("monthly"), "Monthly")
def monthly_line_chart(request): return generate_line_chart(get_date_filter("monthly"), "Monthly")
def monthly_bar_chart(request): return generate_bar_chart(get_date_filter("monthly"), "Monthly")

# Inventory Views
def inventory_main_page(request):
    category_filter = request.GET.get('category', '')
    sort_order = request.GET.get('sort', '')
    items = InventoryItem.objects.all()

    if category_filter:
        items = items.filter(category=category_filter)

    if sort_order == 'expiry':
        items = sorted(
            items,
            key=lambda i: i.expiry_date if hasattr(i, 'expiry_date') and i.expiry_date else datetime.date.max
        )
    else:
        items = items.order_by('-id')

    return render(request, 'inventory_home.html', {
        'is_admin': request.user.isAdmin(),
        'items': items,
        'selected_category': category_filter,
        'selected_sort': sort_order,
    })

def create_inventory_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            item_type = form.cleaned_data['item_type']
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            count = form.cleaned_data['count']

            if item_type == 'perishable':
                expiry_date = form.cleaned_data['expiry_date']
                PerishableInventoryItem.objects.create(
                    name=name,
                    category=category,
                    count=count,
                    expiry_date=expiry_date
                )
            else:
                NonPerishableInventoryItem.objects.create(
                    name=name,
                    category=category,
                    count=count
                )
            messages.success(request, "Item created successfully!")
            return redirect('inventory_home')
    else:
        form = InventoryItemForm()

    return render(request, 'create_inventory_item.html', {'form': form})

def delete_item(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    item.delete()
    messages.success(request, "Item deleted successfully!")
    return redirect('inventory_home')

def test_charts(request):
    return render(request, 'test_charts.html')
