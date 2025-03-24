from django.urls import path

from . import views

urlpatterns = [
    path("", views.inventory_main_page, name="inventory_home"),
    path("create/", views.create_inventory_item, name="create_item"),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
]