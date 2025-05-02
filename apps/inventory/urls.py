from django.urls import path, include
from apps.report_generation.views import reports_page
from . import views

urlpatterns = [
    # Inventory Main View
    path("", views.inventory_home, name="inventory_home"),  # updated to use new inventory_home view
    path("create/", views.create_inventory_item, name="create_item"),
    path("edit/<int:item_id>/", views.edit_item, name="edit_item"),  #  added for edit functionality
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

    # Product-wise Chart Views
    path("charts/product/line/", views.product_line_chart, name="product_line_chart"),
    path("charts/product/histogram/", views.product_histogram, name="product_histogram_chart"),

    # # Test Chart View
    # path("test_charts/", views.test_charts, name="test_charts"),

    # Thresholds
    path("thresholds/", views.threshold_list, name="threshold_list"),
    path("thresholds/edit/<int:pk>/", views.edit_threshold, name="edit_threshold"),
    path("thresholds/delete/<int:pk>/", views.delete_threshold, name="delete_threshold"),
    path("thresholds/add/", views.add_threshold, name="add_threshold"),
]
