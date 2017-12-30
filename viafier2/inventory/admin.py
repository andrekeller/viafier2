from django.contrib import admin
from inventory.models import Article
from inventory.models import Assembly
from inventory.models import Company
from inventory.models import Configuration
from inventory.models import Vehicle


class AssemblyInline(admin.StackedInline):
    extra = 0
    model = Assembly


class ConfigurationInline(admin.StackedInline):
    extra = 0
    model = Configuration


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        ConfigurationInline,
    ]


class ConfigurationAdmin(admin.ModelAdmin):
    inlines = [
        AssemblyInline,
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Assembly)
admin.site.register(Company)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Vehicle)
