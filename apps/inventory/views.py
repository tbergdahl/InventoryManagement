from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PerishableInventoryItemForm, NonPerishableInventoryItemForm
from .models import PerishableInventoryItem
from django.contrib import messages
from django.template.loader import render_to_string

def is_admin(user):
    return user.isAdmin()

def inventory_main_page(request):
    items = PerishableInventoryItem.objects.all()
    return render(request, 'inventory_home.html', {'is_admin' : request.user.isAdmin(), 'items': items})

def create_inventory_item(request):
    if request.method == 'POST':
        form = PerishableInventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the homepage after successful item creation
            return redirect('inventory_home')
    else:
        form = PerishableInventoryItemForm()
    
    return render(request, 'create_inventory_item.html', {'form': form})

def load_form(request):
    form_type = request.GET.get('form_type')
    
    if form_type == 'perish':
        form = PerishableInventoryItemForm()
    elif form_type == 'non-perish':
        form = NonPerishableInventoryItemForm()
    else:
        form = None

    if form:
        html = render_to_string('form.html', {'form': form}, request=request)
        return JsonResponse({'html': html})
    else:
        return JsonResponse({'html': ''})

def delete_item(request, item_id):
    item = get_object_or_404(PerishableInventoryItem, id=item_id)
    item.delete()
    return redirect('inventory_home')