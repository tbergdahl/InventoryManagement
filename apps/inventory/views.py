from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import InventoryItemForm
from .models import PerishableInventoryItem, NonPerishableInventoryItem, InventoryItem

# 'load' function
def inventory_main_page(request):
    # Retrieve all items regardless of type
    items = InventoryItem.objects.all()
    return render(request, 'inventory_home.html', {'is_admin': request.user.isAdmin(), 'items': items})

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
