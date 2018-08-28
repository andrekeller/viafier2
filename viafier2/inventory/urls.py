from functools import partial
from django.urls import path
from django.utils.translation import pgettext_lazy
from django.utils.translation import gettext_lazy
from django.views.generic.base import RedirectView

from inventory.views import InventoryIndex, Rollingstock, RollingstockEngines, RollingstockEngineKlasses

app_name = 'inventory'
urlpatterns = [
    path('', InventoryIndex.as_view(), name='index'),
    path(pgettext_lazy('url', 'rollingstock/'), RedirectView.as_view(pattern_name='inventory:rollingstock-engines', permanent=False), name='rollingstock'),
    path(pgettext_lazy('url', 'rollingstock/coaches'), RollingstockEngines.as_view(), name='rollingstock-coaches'),
    path(pgettext_lazy('url', 'rollingstock/engines'), RollingstockEngines.as_view(), name='rollingstock-engines'),
    path(pgettext_lazy('url', 'rollingstock/engines/<slug:slug>'), RollingstockEngineKlasses.as_view(), name='rollingstock-engines-class'),
    path(pgettext_lazy('url', 'rollingstock/freight-wagons'), RollingstockEngines.as_view(), name='rollingstock-freight-wagons'),
    path(pgettext_lazy('url', 'rollingstock/motor-coaches'), RollingstockEngines.as_view(), name='rollingstock-motor-coaches'),
    path(pgettext_lazy('url', 'rollingstock/service-engines'), RollingstockEngines.as_view(), name='rollingstock-service-engines'),
]
