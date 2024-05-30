from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.timezone import localtime, make_aware

from .models import Building, Room, TimeSlot


def index(request):
    """
    Displays the Dashboard page. For now, this functions returns a placeholder page.
    :param request: The HTTP request.
    :return: An HTTP response containing the dashboard page.
    """
    return render(request, "aubouleau_web/index.html")


def buildings(request):
    """
    Displays the list of all the :py:class:`Building`.
    :param request: The HTTP request.
    :return: An HTTP response containing a page with all the available buildings.
    """
    buildings_list = Building.objects.all()
    return render(request, "aubouleau_web/buildings.html", {"buildings": buildings_list})


def building_detail(request, building_name):
    """
    Displays the detailed information of a :py:class:`Building`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` to show the details for.
    :return: An HTTP response containing the detailed information of the relevant :py:class:`Building`.
    """
    building = get_object_or_404(Building, name=building_name)
    floors_list = building.floor_set.all()
    rooms_list = building.get_all_rooms()
    return render(request, "aubouleau_web/building_detail.html", {"building": building, "floors": floors_list, "rooms": rooms_list})


def building_floors(request, building_name):
    """
    Displays the list of all the :py:class:`Floor` of the relevant :py:class:`Building`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` the :py:class:`Floor` belongs to.
    :return: An HTTP response containing a page with all the available floors of the relevant :py:class:`Building`.
    """
    building = Building.objects.get(name=building_name)
    floors_list = building.floor_set.all()
    return render(request, "aubouleau_web/building_floors.html", {"building": building, "floors": floors_list})


def floor_detail(request, building_name, floor_number):
    """
    Displays the detailed information of a :py:class:`Floor`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` the :py:class:`Floor` belongs to.
    :param floor_number: The number of the :py:class:`Floor` to show the details for.
    :return: An HTTP response containing the detailed information of the relevant :py:class:`Floor`.
    """
    building = Building.objects.get(name=building_name)
    floor = building.floor_set.get(number=floor_number)
    rooms_list = floor.room_set.all()
    return render(request, "aubouleau_web/floor_detail.html", {"building": building, "floor": floor, "rooms": rooms_list})


def floor_rooms(request, building_name, floor_number):
    """
    Displays the list of all the :py:class:`Room` of the relevant :py:class:`Floor`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` the :py:class:`Floor` belongs to.
    :param floor_number: The number of the :py:class:`Floor` to show the details for.
    :return: An HTTP response containing a page with all the available rooms of the relevant :py:class:`Floor`.
    """
    building = Building.objects.get(name=building_name)
    floor = building.floor_set.get(number=floor_number)
    rooms_list = floor.room_set.all()
    return render(request, "aubouleau_web/floor_rooms.html", {"building": building, "floor": floor, "rooms": rooms_list})


def building_rooms(request, building_name):
    """
    Displays the list of all the :py:class:`Room` of the relevant :py:class:`Building`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` the :py:class:`Room` belongs to.
    :return: An HTTP response containing a page with all the available rooms of the relevant :py:class:`Building`.
    """
    building = Building.objects.get(name=building_name)
    rooms_list = building.get_all_rooms()
    return render(request, "aubouleau_web/building_rooms.html", {"building": building, "rooms": rooms_list})


def room_detail(request, building_name, room_number):
    """
    Displays the detailed information of a :py:class:`Room`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` the :py:class:`Room` belongs to.
    :param room_number: The number of the :py:class:`Room` to show the details for.
    :return: An HTTP response containing the detailed information of the relevant :py:class:`Room`.
    """
    building = Building.objects.get(name=building_name)
    room = Room.objects.get(number=room_number)
    time_slots = room.timeslot_set.all().order_by("start_time")

    # A list containing tuples made of 2 elements: (TimeSlot object, True if the time slot is marked as available, False otherwise)
    time_slots_list: list[tuple[TimeSlot, bool]] = []
    previous_time_slot: TimeSlot | None = None

    # If there are no time slots at all, we simply create a single time slot from DAY_START to DAY_END
    if len(time_slots) == 0:
        day_start = make_aware(TimeSlot.DAY_START.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day))
        day_end = make_aware(TimeSlot.DAY_END.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day))
        time_slots_list.append((TimeSlot(subject="Room is available", start_time=day_start, end_time=day_end, created_at=timezone.now(), room=room), True))

    for time_slot in time_slots:
        # If the first time slot of the day stars after DAY_START, add a time slot marked as available that "fills the gap"
        # Since DAY_START is naive, we convert the time_slot start_time to the local time first
        if not previous_time_slot and localtime(time_slot.start_time).time() > TimeSlot.DAY_START.time():
            day_start = make_aware(TimeSlot.DAY_START.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day))
            time_slots_list.append((TimeSlot(subject="Room is available", start_time=day_start, end_time=time_slot.start_time, created_at=timezone.now(), room=time_slot.room), True))
        # If the time_slot does not start where the previous one ended, "fill the gap" with a time slot marked as available
        if previous_time_slot and time_slot.start_time > previous_time_slot.end_time:
            time_slots_list.append((TimeSlot(subject="Room is available", start_time=previous_time_slot.end_time, end_time=time_slot.start_time, created_at=timezone.now(), room=time_slot.room), True))
        time_slots_list.append((time_slot, False))
        previous_time_slot = time_slot

    # If the last time slot of the day ends before DAY_END, add a time slot marked as available that "fills the gap"
    # Since DAY_END is naive, we convert the time_slot end_time to the local time first
    if previous_time_slot and localtime(previous_time_slot.end_time).time() < TimeSlot.DAY_END.time():
        day_end = make_aware(TimeSlot.DAY_END.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day))
        time_slots_list.append((TimeSlot(subject="Room is available", start_time=previous_time_slot.end_time, end_time=day_end, created_at=timezone.now(), room=previous_time_slot.room), True))

    return render(request, "aubouleau_web/room_detail.html", {"building": building, "room": room, "time_slots": time_slots_list})
