from django.db.models import Count
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from inventory.models import Article, Configuration
from django.db.models import Prefetch


class InventoryIndex(PermissionRequiredMixin, ListView):
    model = Article
    permission_required = 'is_staff'
    template_name = 'inventory/index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related(
            'configurations',
            'configurations__vehicle',
            'configurations__vehicle__vehicle',
            'configurations__vehicle__vehicle__klass',
            'configurations__vehicle__vehicle__klass__operator',
            'configurations__assemblies',
            'configurations__assemblies__assembly',
            'configurations__assemblies__assembly__type',
        ).order_by(
        ).filter(
            configurations__isnull=False
        ).annotate(
            configuration_count=Count('configurations'),
            assembly_count=Count('configurations__assemblies')
        ).distinct().extra(
            order_by=[
                'number',
            ]
        )
