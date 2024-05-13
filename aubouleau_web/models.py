from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField("Creation timestamp")

    def __str__(self):
        return f'{self.name}'

    def get_total_floors(self):
        return self.floor_set.count()

    def get_total_rooms(self):
        total_rooms = 0
        for floor in self.floor_set.all():
            total_rooms += floor.get_total_rooms()
        return total_rooms

    def get_all_rooms(self):
        return Room.objects.filter(floor__building=self.id)


class Floor(models.Model):
    number = models.IntegerField("Floor number")
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField("Creation timestamp")
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} (nº{self.number})'

    def get_total_rooms(self):
        return self.room_set.count()

    def get_all_rooms(self):
        return self.room_set.all()


class Room(models.Model):
    number = models.CharField(max_length=8)
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField("Creation timestamp")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} (nº{self.number})'


class EquipmentType(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=80)
    model = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.manufacturer)

    class Meta:
        verbose_name = "Equipment Type"
        verbose_name_plural = "Equipment Types"


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(EquipmentType, on_delete=models.SET_NULL, null=True, blank=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.type)

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"
