from django.contrib import admin
from inventory.models import Article
from inventory.models import Assembly
from inventory.models import Company
from inventory.models import Configuration
from inventory.models import Vehicle


class AssemblyInline(admin.StackedInline):
    extra = 0
    model = Assembly
    raw_id_fields = [
        'assembly',
        'picture',
    ]


class ConfigurationInline(admin.StackedInline):
    extra = 0
    model = Configuration
    raw_id_fields = [
        'vehicle',
        'picture',
    ]


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['number']
    show_full_result_count = False


class AssemblyAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'assembly',
        'picture',
    ]


class ConfigurationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['vehicle', 'article']
    search_fields = ['article__number', 'vehicle__vehicle__number']
    list_per_page = 15
    inlines = [
        AssemblyInline,
    ]
    show_full_result_count = False


class CompanyAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]


class VehicleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['vehicle']
    search_fields = ['vehicle__klass__klass', 'vehicle__number' ]
    show_full_result_count = False


admin.site.register(Article, ArticleAdmin)
admin.site.register(Assembly, AssemblyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Vehicle, VehicleAdmin)
