from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField("Creation timestamp")

    def __str__(self):
        return f'{self.name}'

    def count_floors(self):
        return self.floor_set.count()

    def count_rooms(self):
        total_rooms = 0
        for floor in self.floor_set.all():
            total_rooms += floor.count_rooms()
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

    def count_rooms(self):
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
