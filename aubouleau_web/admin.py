from django.contrib import admin

from .models import Building, Floor, Room, TimeSlot, EquipmentType, Equipment

admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(TimeSlot)
admin.site.register(EquipmentType)
admin.site.register(Equipment)
