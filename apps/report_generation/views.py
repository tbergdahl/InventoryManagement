from django.http import HttpResponse
from apps.inventory.models import InventoryItem
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from datetime import datetime

def reports_page(request):
    if request.method == 'POST':
        # Process form submission and generate report
        report_type = request.POST.get('report_type')
        category = request.POST.get('category')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Get actual report data based on filters
        items = InventoryItem.objects.all()
        if category:
            items = items.filter(category=category)
        if start_date and end_date:
            items = items.filter(expiry_date__range=[start_date, end_date])
        
        context = {
            'report_type': report_type,
            'category': category,
            'start_date': start_date,
            'end_date': end_date,
            'items': items,  # Pass the filtered items to template
            'generated': True
        }
        
        # Check if PDF download was requested
        if 'download_pdf' in request.POST:
            return generate_pdf(request, context)
        
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


from apps.inventory.models import  PerishableInventoryItem

def get_filtered_items(report_type, category=None, start_date=None, end_date=None):
    """
    Returns filtered inventory items with proper polymorphic handling
    """
    # Start with all items
    items = InventoryItem.objects.all()
    
    # Apply category filter if provided
    if category:
        items = items.filter(category=category)
    
    # Apply report-type specific filters
    if report_type == 'expiring_soon':
        # Only work with perishable items
        perishables = PerishableInventoryItem.objects.all()
        if category:
            perishables = perishables.filter(category=category)
        
        # Apply date filters
        perishables = perishables.filter(expiry_date__gte=datetime.now().date())
        if start_date and end_date:
            perishables = perishables.filter(
                expiry_date__range=[start_date, end_date]
            )
        return perishables.order_by('expiry_date')
        
    elif report_type == 'low_stock':
        return items.filter(count__lt=10)
    
    elif report_type == 'category_breakdown':
        return items.order_by('category')
    
    return items  # Default case for inventory_summary

def generate_report_context(report_type, category, start_date, end_date, items):
    """
    Generates context for templates with proper type handling
    """
    items_list = list(items)
    
    return {
        'report_type': {
            'inventory_summary': 'Inventory Summary',
            'expiring_soon': 'Items Expiring Soon',
            'category_breakdown': 'Category Breakdown',
            'low_stock': 'Low Stock Items'
        }.get(report_type, report_type),
        'category': category,
        'start_date': start_date,
        'end_date': end_date,
        'items': items_list,
        'generated': True,
        'report_time': datetime.now()
    }

def generate_pdf(request, context):
    """Generates PDF with proper polymorphic item handling"""
    try:
        html_string = render_to_string('report_pdf.html', context)
        result = BytesIO()
        
        pdf = pisa.pisaDocument(
            BytesIO(html_string.encode("UTF-8")),
            result,
            encoding='UTF-8'
        )
        
        if not pdf.err:
            response = HttpResponse(
                result.getvalue(),
                content_type='application/pdf'
            )
            filename = f"{context['report_type'].replace(' ', '_')}_report.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
            
    except Exception as e:
        print(f"PDF generation error: {e}")
    
    return HttpResponse('Error generating PDF', status=500)

def reports_page(request):
    if request.method == 'POST':
        try:
            report_type = request.POST.get('report_type')
            category = request.POST.get('category')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            
            items = get_filtered_items(report_type, category, start_date, end_date)
            context = generate_report_context(report_type, category, start_date, end_date, items)
            
            if 'download_pdf' in request.POST:
                return generate_pdf(request, context)
            
            return render(request, 'report_output.html', context)
            
        except Exception as e:
            print(f"Report generation error: {e}")
            return render(request, 'error.html', {'error': str(e)})
    
    # GET request - show the filter form
    categories = InventoryItem.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'report_selection.html', {
        'categories': categories,
        'report_types': [
            ('inventory_summary', 'Inventory Summary'),
            ('expiring_soon', 'Items Expiring Soon'),
            ('category_breakdown', 'Category Breakdown'),
            ('low_stock', 'Low Stock Items')
        ]
    })