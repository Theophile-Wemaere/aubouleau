from django.http import HttpResponse
from django.shortcuts import render

from .models import Building, Floor, Room


def index(request):
    return render(request, "aubouleau_web/index.html")


def buildings(request):
    buildings_list = Building.objects.all()
    return render(request, "aubouleau_web/buildings.html", {"buildings": buildings_list})


def building_detail(request, building_name):
    building = Building.objects.get(name=building_name)
    floors_list = building.floor_set.all()
    rooms_list = building.get_all_rooms()
    return render(request, "aubouleau_web/building_detail.html", {"building": building, "floors": floors_list, "rooms": rooms_list})


def floors(request, building_name):
    building = Building.objects.get(name=building_name)
    floors_list = building.floor_set.all()
    return render(request, "aubouleau_web/floors.html", {"building": building, "floors": floors_list})


def floor_detail(request, building_name, floor_number):
    building = Building.objects.get(name=building_name)
    floor = building.floor_set.get(number=floor_number)
    rooms_list = floor.room_set.all()
    return render(request, "aubouleau_web/floor_detail.html", {"building": building, "floor": floor, "rooms": rooms_list})


def rooms(request, building_name):
    building = Building.objects.get(name=building_name)
    rooms_list = building.get_all_rooms()
    return render(request, "aubouleau_web/rooms.html", {"building": building, "rooms": rooms_list})


def room_detail(request, building_name, room_id):
    building = Building.objects.get(name=building_name)
    room = Room.objects.get(pk=room_id)
    return render(request, "aubouleau_web/room_detail.html", {"building": building, "room": room})
