from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=64, unique=True)
    picture = models.CharField(max_length=4096, blank=True, default="")
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
    picture = models.CharField(max_length=4096, blank=True, default="")
    created_at = models.DateTimeField("Creation timestamp")
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} (nº{self.number})'

    def count_rooms(self):
        return self.room_set.count()

    def get_all_rooms(self):
        return self.room_set.all()

    class Meta:
        # A Building can't have two (or more) floors with the same number
        # This guarantees that, for instance, the URL aubouleau.fr/NDC/floors/1 will ALWAYS return a single floor
        # (since the Building NDC can only have one floor with the number 1)
        unique_together = ("number", "building")


class Room(models.Model):
    number = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=64)
    seats = models.IntegerField("Number of seats")
    picture = models.CharField(max_length=4096, blank=True, default="")
    created_at = models.DateTimeField("Creation timestamp")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} (nº{self.number})'
