from django.urls import path

from inventory.views import InventoryIndex

app_name = 'inventory'
urlpatterns = [
    path('', InventoryIndex.as_view(), name='index'),
]
