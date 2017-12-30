from django.contrib import admin
from rollingstock.models import Assembly
from rollingstock.models import AssemblyType
from rollingstock.models import Operator
from rollingstock.models import Vehicle
from rollingstock.models import VehicleKlass

admin.site.register(Assembly)
admin.site.register(AssemblyType)
admin.site.register(Operator)
admin.site.register(Vehicle)
admin.site.register(VehicleKlass)
