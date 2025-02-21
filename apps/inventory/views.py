from django.http import HttpResponse


def inventory_main_page(request):
    return HttpResponse("Inventory Page")