from django.contrib import admin

from .models import *

admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)

admin.site.register(EquipmentType)
admin.site.register(Equipment)
