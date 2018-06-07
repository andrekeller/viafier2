from django.urls import path
from django.views.generic.base import RedirectView

from inventory.views import InventoryIndex, Rollingstock, RollingstockLocomotives

app_name = 'inventory'
urlpatterns = [
    path('index', InventoryIndex.as_view(), name='index'),
    path('rollingstock/', RedirectView.as_view(pattern_name='inventory:rollingstock-locomotives', permanent=False), name='rollingstock'),
    path('rollingstock/locomotives', RollingstockLocomotives.as_view(), name='rollingstock-locomotives')
]
