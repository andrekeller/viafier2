from django.contrib import admin
from rollingstock.models import Assembly
from rollingstock.models import AssemblyType
from rollingstock.models import Operator
from rollingstock.models import Vehicle
from rollingstock.models import VehicleKlass


class VehicleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['klass']
    search_fields = ['klass__klass', 'klass__operator__name', 'klass__operator__abbrev', 'number']

class VehicleKlassAdmin(admin.ModelAdmin):
    search_fields = ['klass', 'operator__name', 'operator__abbrev']

admin.site.register(Assembly)
admin.site.register(AssemblyType)
admin.site.register(Operator)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleKlass, VehicleKlassAdmin)
