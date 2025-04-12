from django.urls import path, include
from apps.report_generation.views import reports_page
from . import views

urlpatterns = [
    # Inventory Main
    path("", views.inventory_main_page, name="inventory_home"),
    path("create/", views.create_inventory_item, name="create_item"),
    path("delete-item/<int:item_id>/", views.delete_item, name="delete_item"),

    # Report Page View
    path("report_generation", reports_page, name="report_generation"),

    # Load Test Data
    path("load-test-data/", views.load_test_data, name="load_test_data"),

    # Weekly Chart Views
    path("charts/weekly/pie/", views.weekly_pie_chart, name="weekly_pie_chart"),
    path("charts/weekly/histogram/", views.weekly_histogram, name="weekly_histogram"),
    path("charts/weekly/line/", views.weekly_line_chart, name="weekly_line_chart"),
    path("charts/weekly/bar/", views.weekly_bar_chart, name="weekly_bar_chart"),

    # Monthly Chart Views
    path("charts/monthly/pie/", views.monthly_pie_chart, name="monthly_pie_chart"),
    path("charts/monthly/histogram/", views.monthly_histogram, name="monthly_histogram"),
    path("charts/monthly/line/", views.monthly_line_chart, name="monthly_line_chart"),
    path("charts/monthly/bar/", views.monthly_bar_chart, name="monthly_bar_chart"),

    # Add test_charts here (merge it in)
    path("test_charts/", views.test_charts, name="test_charts"),
]
