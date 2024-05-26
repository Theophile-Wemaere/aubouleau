from django.shortcuts import render, get_object_or_404

from .models import Building, Floor, Room


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


def floors(request, building_name):
    """
    Displays the list of all the :py:class:`Floor` of the relevant :py:class:`Building`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` the :py:class:`Floor` belongs to.
    :return: An HTTP response containing a page with all the available floors of the relevant :py:class:`Building`.
    """
    building = Building.objects.get(name=building_name)
    floors_list = building.floor_set.all()
    return render(request, "aubouleau_web/floors.html", {"building": building, "floors": floors_list})


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


def rooms(request, building_name):
    """
    Displays the list of all the :py:class:`Room` of the relevant :py:class:`Building`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` the :py:class:`Room` belongs to.
    :return: An HTTP response containing a page with all the available rooms of the relevant :py:class:`Building`.
    """
    building = Building.objects.get(name=building_name)
    rooms_list = building.get_all_rooms()
    return render(request, "aubouleau_web/rooms.html", {"building": building, "rooms": rooms_list})


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
    return render(request, "aubouleau_web/room_detail.html", {"building": building, "room": room})
