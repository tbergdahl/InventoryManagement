from django.http import HttpResponse


def reports_page(request):
    return HttpResponse("reports page")