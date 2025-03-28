from django.http import HttpResponse
from apps.inventory.models import InventoryItem
from django.shortcuts import render


def reports_page(request):
    if request.method == 'POST':
        # Process form submission and generate report
        report_type = request.POST.get('report_type')
        category = request.POST.get('category')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Here you would generate the actual report based on filters
        # For now just showing the selected filters
        context = {
            'report_type': report_type,
            'category': category,
            'start_date': start_date,
            'end_date': end_date,
            'generated': True
        }
        return render(request, 'report_output.html', context)
    
    # GET request - show the filter form
    categories = InventoryItem.objects.values_list('category', flat=True).distinct()
    
    context = {
        'categories': categories,
        'report_types': [
            ('inventory_summary', 'Inventory Summary'),
            ('expiring_soon', 'Items Expiring Soon'),
            ('category_breakdown', 'Category Breakdown'),
            ('low_stock', 'Low Stock Items')
        ]
    }
    return render(request, 'report_selection.html', context)