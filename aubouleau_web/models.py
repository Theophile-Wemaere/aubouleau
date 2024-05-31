import shutil
from datetime import date, datetime, timedelta

from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime, make_aware, is_naive

from aubouleau_web.hpfetch import CALENDARS_DIRECTORY, download_calendars, get_events_of_day


class Building(models.Model):
    """
    A class representing a physical building of ISEP.
    """
    name = models.CharField(max_length=64, unique=True)
    picture = models.CharField(max_length=4096, blank=True, default="")
    created_at = models.DateTimeField("Creation timestamp")

    def __str__(self):
        return f'{self.name}'

    def count_floors(self):
        """
        Counts the amount of floors contained in this :py:class:`Building`.
        :return: The number of floors of this :py:class:`Building`.
        """
        return self.floor_set.count()

    def count_rooms(self):
        """
        Counts the amount of rooms contained in this :py:class:`Building`.
        :return: The number of rooms of this :py:class:`Building`.
        """
        total_rooms = 0
        for floor in self.floor_set.all():
            total_rooms += floor.count_rooms()
        return total_rooms

    def count_available_rooms(self) -> int:
        """
        Counts the amount of rooms that are available right now.
        :return: The number of available rooms in this :py:class:`Building`.
        """
        rooms = self.get_all_rooms()
        available_rooms = 0
        for room in rooms:
            if room.is_available():
                available_rooms += 1
        return available_rooms

    def count_unavailable_rooms(self) -> int:
        """
        Counts the amount of rooms that are unavailable right now.
        :return: The number of unavailable rooms in this :py:class:`Building`.
        """
        rooms = self.get_all_rooms()
        unavailable_rooms = 0
        for room in rooms:
            if room.is_unavailable():
                unavailable_rooms += 1
        return unavailable_rooms

    def get_all_rooms(self):
        """
        Fetches all the rooms contained in this :py:class:`Building`.
        :return: A list of all the :py:class:`Room` contained in this :py:class:`Building`.
        """
        return Room.objects.filter(floor__building=self.id)


class Floor(models.Model):
    """
    A class representing a physical floor of a :py:class:`Building`.
    """
    number = models.IntegerField("Floor number")
    name = models.CharField(max_length=64)
    picture = models.CharField(max_length=4096, blank=True, default="")
    created_at = models.DateTimeField("Creation timestamp")
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.number})'

    def count_rooms(self):
        """
        Counts the amount of rooms contained in this :py:class:`Floor`.
        :return: The number of rooms of this :py:class:`Floor`.
        """
        return self.room_set.count()

    def get_all_rooms(self):
        """
        Fetches all the rooms contained in this :py:class:`Floor`.
        :return: A list of all the :py:class:`Room` contained in this :py:class:`Floor`.
        """
        return self.room_set.all()

    class Meta:
        # A Building can't have two (or more) floors with the same number
        # This guarantees that, for instance, the URL aubouleau.fr/NDC/floors/1 will ALWAYS return a single floor
        # (since the Building NDC can only have one floor with the number 1)
        unique_together = ("number", "building")


class Room(models.Model):
    """
    A class representing a physical room of a :py:class:`Floor`.
    """
    number = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=64)
    seats = models.IntegerField("Number of seats")
    picture = models.CharField(max_length=4096, blank=True, default="")
    created_at = models.DateTimeField("Creation timestamp")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.number} ({self.name})'

    def is_available(self) -> bool:
        """
        Indicates if this room is available right now.
        :return: True if the room is available, False otherwise.
        """
        time_slots = self.timeslot_set.all().order_by("start_time")
        now = timezone.now()
        for time_slot in time_slots:
            if time_slot.start_time <= now <= time_slot.end_time:
                return False
        return True

    def is_available_at(self, time: datetime) -> bool:
        """
        Indicates if this room is available at the provided time.
        :param time: The time to check the availability for.
        :return: True if this room is available at the provided time, False otherwise.
        """
        time_slots = self.timeslot_set.all().order_by("start_time")
        for time_slot in time_slots:
            if time_slot.start_time <= time <= time_slot.end_time:
                return False
        return True

    def is_available_soon(self, minutes=60) -> bool:
        """
        Indicates if this room will become available in less than the provided amount of minutes.
        :param minutes: The number of minutes at which the room is considered NOT available soon (default is 60)
        :return: True if the room will be available in less than the provided amount of minutes (or if it's already available), False otherwise.
        """
        time_slot = self.get_current_time_slot()
        if time_slot and (time_slot.end_time - timezone.now()) < timedelta(minutes=minutes):
            return True
        # Room is already available
        if not time_slot:
            return True
        return False

    def get_time_left_until_available(self) -> timedelta:
        """
        Calculates the amount of time left until this room is available.
        :return: A :py:class:`datetime` object representing the amount of time left until this room is available.
        """
        time_slots = self.timeslot_set.all().order_by("start_time")
        now = timezone.now()
        for time_slot in time_slots:
            # Find the current time slot
            if time_slot.start_time <= now <= time_slot.end_time:
                return time_slot.end_time - now
        return timedelta()

    def is_unavailable(self) -> bool:
        """
        Convenient shortcut method that returns the opposite of :py:meth:`Room.is_available`.
        :return: True is the room is unavailable, False otherwise.
        """
        return not self.is_available()

    def get_current_time_slot(self):
        time_slots = self.timeslot_set.all().order_by("start_time")
        now = timezone.now()
        for time_slot in time_slots:
            if time_slot.start_time <= now <= time_slot.end_time:
                return time_slot
        return None


class TimeSlot(models.Model):
    """
    A class representing a time slot in the planning of a :py:class:`Room`.
    """
    # These variables define the boundaries of the schedule displayed for each room
    DAY_START = datetime(2000, 1, 1, 8, 0, 0, 0)
    DAY_END = datetime(2000, 1, 1, 20, 0, 0, 0)

    subject = models.CharField(max_length=512, verbose_name="Subject name")
    start_time = models.DateTimeField("Start time")
    end_time = models.DateTimeField("End time")
    created_at = models.DateTimeField("Creation timestamp")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.room.number}] {localtime(self.start_time).strftime("%d/%m/%Y, %H:%M")} - {localtime(self.end_time).strftime("%H:%M")} | {self.subject}'

    @staticmethod
    def update_time_slots() -> None:
        """
        Deletes all stored calendars and time slots and forces the re-download of calendars.
        New :py:class:`TimeSlot` objects are created from the newly downloaded calendars.
        """
        # Delete all the calendars to force re-download
        shutil.rmtree(CALENDARS_DIRECTORY, ignore_errors=True)

        # Fetch all the room numbers from the DB and download all calendars
        room_numbers = Room.objects.values_list("number", flat=True)
        download_calendars(room_numbers)

        # Delete all time slots to ensure there are no duplicates
        TimeSlot.objects.all().delete()

        for room_number in room_numbers:
            print(f'Creating time slots for room {room_number}...', end="", flush=True)

            # If the room does not exist in the application, skip it
            try:
                room = Room.objects.get(number=room_number)
            except Room.DoesNotExist:
                continue

            events = get_events_of_day(room_number, date.today())
            for event in events:
                # Extract the three values from the tuple
                # All naive datetime objects are converted to aware datetime objects
                start_datetime, end_datetime, subject = make_aware(event[0]) if is_naive(event[0]) else event[0], make_aware(event[1]) if is_naive(event[1]) else event[1], event[2]
                room.timeslot_set.create(subject=subject, start_time=start_datetime, end_time=end_datetime, created_at=timezone.now())
            print("\t[OK]")
        print("All time slots have been successfully created.")


# This is stupid, but there is no way to make django-crontab call a static method from a class (the function to call must not be in a class)
# This is due to the way django-crontab parses the settings.CRONJOBS list, see: https://github.com/kraiz/django-crontab/blob/master/django_crontab/crontab.py#L169-L172
def update_time_slots():
    TimeSlot.update_time_slots()
