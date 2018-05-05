from django.contrib import admin
from nested_admin import NestedStackedInline
from nested_admin import NestedModelAdmin
from inventory.models import Article
from inventory.models import Assembly
from inventory.models import Company
from inventory.models import Configuration
from inventory.models import Vehicle


class AssemblyNestedInline(NestedStackedInline):
    extra = 0
    model = Assembly
    raw_id_fields = [
        'assembly',
        'picture',
    ]


class ConfigurationInline(NestedStackedInline):
    extra = 0
    model = Configuration
    inlines = [
        AssemblyNestedInline,
    ]
    raw_id_fields = [
        'vehicle',
        'picture',
    ]

    #def get_queryset(self, request):
    #    qs = super().get_queryset(request)
    #    return qs.select_related()


class ArticleAdmin(NestedModelAdmin):
    inlines = [
        ConfigurationInline,
    ]
    #raw_id_fields = [
    #    'manufacturer',
    #    'vendor',
    #]
    show_full_result_count = False


class ConfigurationAdmin(NestedModelAdmin):
    inlines = [
        AssemblyNestedInline,
    ]
    show_full_result_count = False


class VehicleAdmin(admin.ModelAdmin):
    show_full_result_count = False


admin.site.register(Article, ArticleAdmin)
admin.site.register(Assembly)
admin.site.register(Company)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Vehicle, VehicleAdmin)
