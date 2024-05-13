from django.http import HttpResponse
from django.shortcuts import render

from .models import *


def index(request):
    return render(request, "aubouleau_web/index.html")


def buildings(request):
    buildings_list = Building.objects.all()
    return render(request, "aubouleau_web/buildings.html", {"buildings": buildings_list})


def building_detail(request, building_id):
    building = Building.objects.get(pk=building_id)
    floors_list = building.floor_set.all()
    rooms_list = building.get_all_rooms()
    return render(request, "aubouleau_web/building_detail.html", {"building": building, "floors": floors_list, "rooms": rooms_list})


def floors(request, building_id):
    building = Building.objects.get(pk=building_id)
    floors_list = building.floor_set.all()
    return render(request, "aubouleau_web/floors.html", {"building": building, "floors": floors_list})


def floor_detail(request, building_id, floor_id):
    building = Building.objects.get(pk=building_id)
    floor = Floor.objects.get(pk=floor_id)
    rooms_list = floor.room_set.all()
    return render(request, "aubouleau_web/floor_detail.html", {"building": building, "floor": floor, "rooms": rooms_list})


def rooms(request, building_id):
    building = Building.objects.get(pk=building_id)
    rooms_list = building.get_all_rooms()
    return render(request, "aubouleau_web/rooms.html", {"building": building, "rooms": rooms_list})


def room_detail(request, building_id, room_id):
    building = Building.objects.get(pk=building_id)
    room = Room.objects.get(pk=room_id)
    return render(request, "aubouleau_web/room_detail.html", {"building": building, "room": room})


def building_equipment(request, building_id):
    building = Building.objects.get(pk=building_id)
    # TODO: replace with method from the Building model
    equipment_list = Equipment.objects.all()
    return render(request, 'aubouleau_web/building_equipment.html', {"building": building, "equipment_list": equipment_list})
