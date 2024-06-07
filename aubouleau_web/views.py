from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.utils.timezone import localtime, make_aware

from .models import Building, Floor, Room, TimeSlot, Equipment, EquipmentType, Problem, Comment


def index(request):
    """
    Displays the Dashboard page. For now, this functions returns a placeholder page.
    :param request: The HTTP request.
    :return: An HTTP response containing the dashboard page.
    """
    buildings = Building.objects.all()
    problems = Problem.objects.filter(status='OPEN').order_by('-created_at')

    available_rooms, unavailable_rooms = 0, 0
    for building in buildings:
        available_rooms += building.count_available_rooms()
        unavailable_rooms += building.count_unavailable_rooms()

    rooms = Room.objects.all()

    # Each tuple contains: the room soon available, its current time slot, the time left until available (in minutes) and the string "Updated [time] agp"
    rooms_soon_available: list[tuple[Room, TimeSlot, int, str]] = []
    for room in rooms:
        if room.is_available_soon() and room.get_time_left_until_available().seconds > 0:
            time_slot = room.get_current_time_slot()
            last_update_time = timezone.now() - time_slot.created_at
            if (last_update_time.seconds / 60) > 59:
                update_info = f"Updated {round(last_update_time.seconds / 3600)} hour{'s' if round(last_update_time.seconds / 3600) > 1 else ''} ago"
            else:
                update_info = f"Updated {round(last_update_time.seconds / 60)} minute{'s' if round(last_update_time.seconds / 60) > 1 else ''} ago"
            rooms_soon_available.append((room, time_slot, round(room.get_time_left_until_available().seconds / 60), update_info))
    # Sort rooms soon available based on the time left until available (increasing order)
    sorted_rooms_soon_available = sorted(rooms_soon_available, key=lambda x: x[2])

    # Each tuple contains: the room soon unavailable, its next time slot, the time left until the room is unavailable (in minutes) and the string "Updated [time] ago"
    rooms_soon_unavailable: list[tuple[Room, TimeSlot, int, str]] = []
    for room in rooms:
        if room.is_unavailable_soon() and room.get_time_left_until_unavailable() and room.get_time_left_until_unavailable().seconds > 0:
            next_time_slot = room.get_next_time_slot()
            last_update_time = timezone.now() - next_time_slot.created_at
            if (last_update_time.seconds / 60) > 59:
                update_info = f"Updated {round(last_update_time.seconds / 3600)} hour{'s' if round(last_update_time.seconds / 3600) > 1 else ''} ago"
            else:
                update_info = f"Updated {round(last_update_time.seconds / 60)} minute{'s' if round(last_update_time.seconds / 60) > 1 else ''} ago"
            rooms_soon_unavailable.append((room, next_time_slot, round(room.get_time_left_until_unavailable().seconds / 60), update_info))
    # Sort rooms soon unavailable based on the time left until unavailable (increasing order)
    sorted_rooms_soon_unavailable = sorted(rooms_soon_unavailable, key=lambda x: x[2])

    return render(request, "aubouleau_web/index.html", {"problems": problems , "available_rooms": available_rooms, "unavailable_rooms": unavailable_rooms, "rooms_soon_available": sorted_rooms_soon_available, "rooms_soon_unavailable": sorted_rooms_soon_unavailable})


def sign_in(request):
    """
    Displays the sign-in page.
    :param request: The HTTP request.
    :return: An HTTP response containing a page with the sign-in form.
    """
    if request.method == 'GET':
        return render(request, "aubouleau_web/sign_in.html", {"next_url": request.GET.get('next', None)})
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next_url', None)
            if next_url:
                return redirect(next_url)
            else:
                return redirect("aubouleau_web:index")
        else:
            return render(request, "aubouleau_web/sign_in.html", {"invalid_credentials": True})
    else:
        return render(request, status=405, template_name="405.html")


def sign_up(request):
    """
    Displays the sign-up page.
    :param request: The HTTP request.
    :return: An HTTP response containing a page with the sign-up form.
    """
    if request.method == 'GET':
        return render(request, "aubouleau_web/sign_up.html")
    elif request.method == 'POST':
        # TODO: If there's time, server-side validation
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        password = request.POST.get('password', None)
        password_confirm = request.POST.get('password_confirm', None)

        # Create the user, log it in and redirect to the dashboard page
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        login(request, user)
        return redirect("aubouleau_web:index")
    else:
        return render(request, status=405, template_name="405.html")


def sign_out(request):
    """
    Logs the user out (destroys its session) and redirects to the dashboard page.
    :param request: The HTTP request.
    :return: An HTTP 302 response to the dashboard page.
    """
    if request.method == 'GET':
        logout(request)
        return redirect("aubouleau_web:index")
    else:
        return render(request, status=405, template_name="405.html")


@login_required
def administration_buildings(request):
    """
    Displays the buildings administration page.
    :param request: The HTTP request.
    :return: An HTTP response containing a page where buildings are displayed and can be modified.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    buildings_list = Building.objects.all().order_by('name')

    return render(request, "aubouleau_web/administration_buildings.html", {"buildings": buildings_list})


@login_required()
def administration_buildings_new(request):
    """
    Displays the page containing a form to add a new building
    :param request: The HTTP request.
    :return: An HTTP response containing a page with a form to add a new building.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'GET':
        return render(request, "aubouleau_web/administration_buildings_new.html")
    elif request.method == 'POST':
        building_name = request.POST.get('building_name', None)
        # TODO: Handle building picture upload
        Building.objects.create(name=building_name, created_at=timezone.now())
        return redirect("aubouleau_web:administration_buildings")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def administration_buildings_edit(request, building_name):
    """
    Displays the page containing a form to edit an existing building
    :param request: The HTTP request.
    :param building_name: The name of the building to edit.
    :return: An HTTP response containing a page with a form to edit an existing building
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'GET':
        building = Building.objects.get(name=building_name)
        return render(request, "aubouleau_web/administration_buildings_edit.html", {"building": building})
    elif request.method == 'POST':
        building = Building.objects.get(name=building_name)
        building_name = request.POST.get('building_name', None)
        # TODO: Handle building picture upload
        building.name = building_name
        building.save()
        return redirect("aubouleau_web:administration_buildings")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def administration_buildings_delete(request, building_name):
    """
    Deletes an existing building from the database. This method only handles POST requests.
    :param request: The HTTP request.
    :param building_name: The name of the building to delete.
    :return: An HTTP 302 response to the buildings administration page.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()
    
    if request.method == 'POST':
        building = Building.objects.get(name=building_name)
        building.delete()
        return redirect("aubouleau_web:administration_buildings")
    else:
        return render(request, status=405, template_name="405.html")


@login_required
def administration_floors(request):
    """
    Displays the floors administration page.
    :param request: The HTTP request.
    :return: An HTTP response containing a page where floors are displayed and can be modified.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    floors_list = Floor.objects.all().order_by('building')

    return render(request, "aubouleau_web/administration_floors.html", {"floors": floors_list})


@login_required()
def administration_floors_new(request):
    """
    Displays the page containing a form to add a new floor
    :param request: The HTTP request.
    :return: An HTTP response containing a page with a form to add a new floor.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'GET':
        buildings_list = Building.objects.all()
        return render(request, "aubouleau_web/administration_floors_new.html", {"buildings": buildings_list})
    elif request.method == 'POST':
        floor_name = request.POST.get('floor_name', None)
        floor_number = request.POST.get('floor_number', None)
        floor_building_id = request.POST.get('floor_building_id', None)
        Floor.objects.create(name=floor_name, number=floor_number, building=Building.objects.get(pk=floor_building_id), created_at=timezone.now())
        return redirect("aubouleau_web:administration_floors")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def administration_floors_edit(request, building_name, floor_number):
    """
    Displays the page containing a form to edit an existing floor
    :param request: The HTTP request.
    :param building_name: The name of the floor's building.
    :param floor_number: The number of the floor to edit.
    :return: An HTTP response containing a page with a form to edit an existing floor
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'GET':
        buildings_list = Building.objects.all()
        building = Building.objects.get(name=building_name)
        floor = building.floor_set.get(number=floor_number)
        return render(request, "aubouleau_web/administration_floors_edit.html", {"buildings": buildings_list, "floor": floor})
    elif request.method == 'POST':
        building = Building.objects.get(name=building_name)
        floor = building.floor_set.get(number=floor_number)
        floor_name = request.POST.get('floor_name', None)
        floor_number = request.POST.get('floor_number', None)
        floor_building_id = request.POST.get('floor_building_id', None)

        floor.name = floor_name
        floor.number = floor_number
        floor.building = Building.objects.get(pk=floor_building_id)
        floor.save()
        return redirect("aubouleau_web:administration_floors")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def administration_floors_delete(request, building_name, floor_number):
    """
    Deletes an existing floor from the database. This method only handles POST requests.
    :param request: The HTTP request.
    :param building_name: The name of the floor's building.
    :param floor_number: The number of the floor to delete.
    :return: An HTTP 302 response to the floors administration page.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'POST':
        building = Building.objects.get(name=building_name)
        floor = building.floor_set.get(number=floor_number)
        floor.delete()
        return redirect("aubouleau_web:administration_floors")
    else:
        return render(request, status=405, template_name="405.html")


@login_required
def administration_rooms(request):
    """
    Displays the rooms administration page.
    :param request: The HTTP request.
    :return: An HTTP response containing a page where rooms are displayed and can be modified.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    rooms_list = Room.objects.all().order_by('floor')

    return render(request, "aubouleau_web/administration_rooms.html", {"rooms": rooms_list})


@login_required()
def administration_rooms_new(request):
    """
    Displays the page containing a form to add a new room
    :param request: The HTTP request.
    :return: An HTTP response containing a page with a form to add a new room.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'GET':
        floors_list = Floor.objects.all().order_by('building')
        return render(request, "aubouleau_web/administration_rooms_new.html", {"floors": floors_list})
    elif request.method == 'POST':
        room_number = request.POST.get('room_number', None)
        room_name = request.POST.get('room_name', None)
        seats = request.POST.get('seats', None)
        # TODO: Handle room picture upload
        room_floor_id = request.POST.get('room_floor_id', None)

        Room.objects.create(number=room_number, name=room_name, seats=seats, floor=Floor.objects.get(pk=room_floor_id), created_at=timezone.now())
        return redirect("aubouleau_web:administration_rooms")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def administration_rooms_edit(request, room_number):
    """
    Displays the page containing a form to edit an existing room
    :param request: The HTTP request.
    :param room_number: The number of the room to edit.
    :return: An HTTP response containing a page with a form to edit an existing room
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'GET':
        floors_list = Floor.objects.all().order_by('building')
        room = Room.objects.get(number=room_number)
        return render(request, "aubouleau_web/administration_rooms_edit.html", {"floors": floors_list, "room": room})
    elif request.method == 'POST':
        room = Room.objects.get(number=room_number)
        room_number = request.POST.get('room_number', None)
        room_name = request.POST.get('room_name', None)
        seats = request.POST.get('seats', None)
        room_floor_id = request.POST.get('room_floor_id', None)
        # TODO: Handle room picture upload

        room.number = room_number
        room.name = room_name
        room.seats = seats
        room.floor = Floor.objects.get(pk=room_floor_id)
        room.save()
        return redirect("aubouleau_web:administration_rooms")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def administration_rooms_delete(request, room_number):
    """
    Deletes an existing room from the database. This method only handles POST requests.
    :param request: The HTTP request.
    :param room_number: The number of the room to delete.
    :return: An HTTP 302 response to the rooms administration page.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'POST':
        room = Room.objects.get(number=room_number)
        room.delete()
        return redirect("aubouleau_web:administration_rooms")
    else:
        return render(request, status=405, template_name="405.html")


@login_required
def administration_equipment(request):
    """
    Displays the equipment administration page.
    :param request: The HTTP request.
    :return: An HTTP response containing a page where equipment is displayed and can be modified.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    equipment_list = Equipment.objects.all().order_by('room')

    return render(request, "aubouleau_web/administration_equipment.html", {"equipment_list": equipment_list})


@login_required()
def administration_equipment_new(request):
    """
    Displays the page containing a form to add a new piece of equipment
    :param request: The HTTP request.
    :return: An HTTP response containing a page with a form to add a new piece of equipment.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'GET':
        equipment_type_list = EquipmentType.objects.all().order_by('name')
        rooms_list = Room.objects.all().order_by('floor')
        return render(request, "aubouleau_web/administration_equipment_new.html", {"equipment_types": equipment_type_list, "rooms": rooms_list})
    elif request.method == 'POST':
        equipment_name = request.POST.get('equipment_name', None)
        equipment_manufacturer = request.POST.get('equipment_manufacturer', None)
        equipment_model = request.POST.get('equipment_model', None)
        equipment_type_id = request.POST.get('equipment_type_id', None)
        equipment_room_id = request.POST.get('equipment_room_id', None)
        # TODO: Handle equipment picture upload
        Equipment.objects.create(name=equipment_name, manufacturer=equipment_manufacturer, model=equipment_model, type=EquipmentType.objects.get(pk=equipment_type_id), room=Room.objects.get(pk=equipment_room_id), created_at=timezone.now())
        return redirect("aubouleau_web:administration_equipment")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def administration_equipment_edit(request, equipment_id):
    """
    Displays the page containing a form to edit an existing piece of equipment
    :param request: The HTTP request.
    :param equipment_id: The id of the piece of equipment to edit.
    :return: An HTTP response containing a page with a form to edit an existing piece of equipment
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'GET':
        equipment = Equipment.objects.get(pk=equipment_id)
        equipment_type_list = EquipmentType.objects.all().order_by('name')
        rooms_list = Room.objects.all().order_by('floor')
        return render(request, "aubouleau_web/administration_equipment_edit.html", {"equipment_types": equipment_type_list, "rooms": rooms_list, "equipment": equipment})
    elif request.method == 'POST':
        equipment = Equipment.objects.get(pk=equipment_id)
        equipment_name = request.POST.get('equipment_name', None)
        equipment_manufacturer = request.POST.get('equipment_manufacturer', None)
        equipment_model = request.POST.get('equipment_model', None)
        # TODO: Handle equipment picture upload
        equipment_type_id = request.POST.get('equipment_type_id', None)
        equipment_room_id = request.POST.get('equipment_room_id', None)

        equipment.name = equipment_name
        equipment.manufacturer = equipment_manufacturer
        equipment.model = equipment_model
        equipment.type = EquipmentType.objects.get(pk=equipment_type_id)
        equipment.room = Room.objects.get(pk=equipment_room_id)
        equipment.save()
        return redirect("aubouleau_web:administration_equipment")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def administration_equipment_delete(request, equipment_id):
    """
    Deletes an existing piece of equipment from the database. This method only handles POST requests.
    :param request: The HTTP request.
    :param equipment_id: The id of the piece of equipment to delete.
    :return: An HTTP 302 response to the equipment administration page.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'POST':
        equipment = Equipment.objects.get(pk=equipment_id)
        equipment.delete()
        return redirect("aubouleau_web:administration_equipment")
    else:
        return render(request, status=405, template_name="405.html")


@login_required
def administration_equipment_types(request):
    """
    Displays the equipment types administration page.
    :param request: The HTTP request.
    :return: An HTTP response containing a page where equipment types are displayed and can be modified.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    equipment_types_list = EquipmentType.objects.all().order_by('name')

    return render(request, "aubouleau_web/administration_equipment_types.html", {"equipment_types": equipment_types_list})


@login_required()
def administration_equipment_types_new(request):
    """
    Displays the page containing a form to add a new equipment type
    :param request: The HTTP request.
    :return: An HTTP response containing a page with a form to add a new equipment type.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'GET':
        return render(request, "aubouleau_web/administration_equipment_types_new.html")
    elif request.method == 'POST':
        equipment_type_name = request.POST.get('equipment_type_name', None)
        # TODO: Handle equipment type picture upload
        EquipmentType.objects.create(name=equipment_type_name, created_at=timezone.now())
        return redirect("aubouleau_web:administration_equipment_types")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def administration_equipment_types_edit(request, equipment_type_name):
    """
    Displays the page containing a form to edit an existing equipment type
    :param request: The HTTP request.
    :param equipment_type_name: The name of the equipment type to edit.
    :return: An HTTP response containing a page with a form to edit an existing equipment type
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'GET':
        equipment_type = EquipmentType.objects.get(name=equipment_type_name)
        return render(request, "aubouleau_web/administration_equipment_types_edit.html", {"equipment_type": equipment_type})
    elif request.method == 'POST':
        equipment_type = EquipmentType.objects.get(name=equipment_type_name)
        equipment_type_name = request.POST.get('equipment_type_name', None)
        # TODO: Handle equipment picture upload

        equipment_type.name = equipment_type_name
        equipment_type.save()
        return redirect("aubouleau_web:administration_equipment_types")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def administration_equipment_types_delete(request, equipment_type_name):
    """
    Deletes an existing equipment type from the database. This method only handles POST requests.
    :param request: The HTTP request.
    :param equipment_type_name: The name of the equipment type to delete.
    :return: An HTTP 302 response to the equipment types administration page.
    """
    # This is not the best way to manage permissions, but for the scope of this application, checking that the
    # user is a member of the "Administrators" group is enough.
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'POST':
        equipment_type = EquipmentType.objects.get(name=equipment_type_name)
        equipment_type.delete()
        return redirect("aubouleau_web:administration_equipment_types")
    else:
        return render(request, status=405, template_name="405.html")


def problems(request):
    """
    Displays the list of all the :py:class:`Problem` with the "OPEN" status.
    :param request: The HTTP request.
    :return: An HTTP response containing a page with all the open problems.
    """
    open_problems_list = Problem.objects.filter(status='OPEN').order_by('-created_at')
    return render(request, "aubouleau_web/problems.html", {"problems": open_problems_list})


def problems_closed(request):
    """
    Displays the list of all the :py:class:`Problem` with the "CLOSED" or "SOLVED" status.
    :param request: The HTTP request.
    :return: An HTTP response containing a page with all the closed problems.
    """
    closed_problems_list = Problem.objects.filter(Q(status='SOLVED') | Q(status='CLOSED')).order_by('id')
    return render(request, "aubouleau_web/problems_closed.html", {"problems": closed_problems_list})


def problem_detail(request, problem_id):
    """
    Displays the details of a specific :py:class:`Problem`.
    :param request: The HTTP request.
    :param problem_id: The id of the problem to display the details of.
    :return: An HTTP response containing a page with the details of the problem.
    """
    problem = Problem.objects.get(pk=problem_id)
    comments = problem.comment_set.all().order_by('created_at')
    return render(request, "aubouleau_web/problem_detail.html", {"problem": problem, "comments": comments})


@login_required()
def problems_new(request):
    """
    Displays the page containing a form to report a new problem
    :param request: The HTTP request.
    :return: An HTTP response containing a page with a form to report a new problem.
    """
    if request.method == 'GET':
        rooms_list = Room.objects.all().order_by('floor')
        equipment_list = Equipment.objects.all().order_by('type')
        return render(request, "aubouleau_web/problems_new.html", {"rooms": rooms_list, "equipment_list": equipment_list})
    elif request.method == 'POST':
        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        room_id = request.POST.get('room_id', None)
        equipment_id = request.POST.get('equipment_id', None)

        # TODO: Fix this terribleness
        # For the sake of your eyes, skip to line 675
        # Proper server side validation would be way better, yes, but this will do it for now
        if room_id == '':
            room_id = None
        if equipment_id == '':
            equipment_id = None

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            room = None
        try:
            equipment = Equipment.objects.get(pk=equipment_id)
        except Equipment.DoesNotExist:
            equipment = None

        if (not room and not equipment) or (room and equipment):
            return render(request, status=400, template_name="400.html")

        Problem.objects.create(status='OPEN', title=title, description=description, reporter=request.user, room=room, equipment=equipment, created_at=timezone.now())
        return redirect("aubouleau_web:problems")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def problems_solve(request, problem_id):
    """
    Marks an existing :py:class:`Problem` as "SOLVED". This method only handles POST requests.
    :param request: The HTTP request.
    :param problem_id: The id of the problem to mark as "SOLVED".
    :return: An HTTP 302 to the problem detail page.
    """
    problem = Problem.objects.get(pk=problem_id)
    # Only administrators can solve problems
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'POST':
        problem.mark_solved(solved_by=request.user)
        return redirect("aubouleau_web:problem_detail", problem_id=problem_id)
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def problems_close(request, problem_id):
    """
    Marks an existing :py:class:`Problem` as "CLOSED". This method only handles POST requests.
    :param request: The HTTP request.
    :param problem_id: The id of the problem to mark as "CLOSED".
    :return: An HTTP 302 to the problem detail page.
    """
    problem = Problem.objects.get(pk=problem_id)
    # Only administrators can solve problems
    if not request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'POST':
        problem.mark_closed(closed_by=request.user)
        return redirect("aubouleau_web:problem_detail", problem_id=problem_id)
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def problems_delete(request, problem_id):
    """
    Deletes an existing :py:class:`Problem`. This method only handles POST requests.
    :param request: The HTTP request.
    :param problem_id: The id of the problem to delete.
    :return: An HTTP 302 to the problems page.
    """
    problem = Problem.objects.get(pk=problem_id)
    # Only the problem's reporter or administrators can delete problems
    if request.user != problem.reporter and request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'POST':
        problem.delete()
        return redirect("aubouleau_web:problems")
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def problems_comment_add(request, problem_id):
    """
    Adds a comment to an existing :py:class:`Problem`. This method only handles POST requests.
    :param request: The HTTP request.
    :param problem_id: The id of the problem to add a comment on.
    :return: An HTTP 302 to the detail page of the problem.
    """
    if request.method == 'POST':
        problem = Problem.objects.get(pk=problem_id)

        # Prevent comments from being posted on closed or resolved issues.
        if not problem.is_open():
            raise PermissionDenied()

        text = request.POST.get('comment', None)
        author = User.objects.get(pk=request.user.id)
        problem.comment_set.create(text=text, author=author, created_at=timezone.now())
        return redirect("aubouleau_web:problem_detail", problem_id=problem_id)
    else:
        return render(request, status=405, template_name="405.html")


@login_required()
def problems_comment_delete(request, problem_id, comment_id):
    """
    Deletes a comment from an existing :py:class:`Problem`. This method only handles POST requests.
    :param request: The HTTP request.
    :param problem_id: The id of the problem the comment is attached to.
    :param comment_id: The id of the comment to delete.
    :return: An HTTP 302 to the detail page of the problem.
    """
    comment = Comment.objects.get(pk=comment_id)
    # Only the comment's author or administrators can delete comments
    if request.user != comment.author and request.user.groups.filter(name="Administrators").exists():
        raise PermissionDenied()

    if request.method == 'POST':
        comment.delete()
        return redirect("aubouleau_web:problem_detail", problem_id=problem_id)
    else:
        return render(request, status=405, template_name="405.html")


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
    equipment_list = building.get_all_equipment()
    return render(request, "aubouleau_web/building_detail.html", {"building": building, "floors": floors_list, "rooms": rooms_list, "equipment_list": equipment_list})


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
    equipment_list = floor.get_all_equipment()
    return render(request, "aubouleau_web/floor_detail.html", {"building": building, "floor": floor, "rooms": rooms_list, "equipment_list": equipment_list})


def floor_rooms(request, building_name, floor_number):
    """
    Displays the list of all the :py:class:`Room` of the relevant :py:class:`Floor`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` the :py:class:`Floor` belongs to.
    :param floor_number: The number of the :py:class:`Floor` to show the rooms of.
    :return: An HTTP response containing a page with all the available rooms of the relevant :py:class:`Floor`.
    """
    building = Building.objects.get(name=building_name)
    floor = building.floor_set.get(number=floor_number)
    rooms_list = floor.room_set.all()
    return render(request, "aubouleau_web/floor_rooms.html", {"building": building, "floor": floor, "rooms": rooms_list})


def floor_equipment(request, building_name, floor_number):
    """
    Displays the list of all the :py:class:`Equipment` of the relevant :py:class:`Floor`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` the :py:class:`Floor` belongs to.
    :param floor_number: The number of the :py:class:`Floor` to show the equipment of.
    :return: An HTTP response containing a page with all the available equipment of the relevant :py:class:`Floor`.
    """
    building = Building.objects.get(name=building_name)
    floor = building.floor_set.get(number=floor_number)
    equipment_list = floor.get_all_equipment()
    return render(request, "aubouleau_web/floor_equipment.html", {"building": building, "floor": floor, "equipment_list": equipment_list})


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
    problems = room.problem_set.filter(status='OPEN').order_by("-created_at")

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

    return render(request, "aubouleau_web/room_detail.html", {"building": building, "room": room, "time_slots": time_slots_list, "problems": problems})


def building_equipment(request, building_name):
    """
    Displays the list of all the :py:class:`Equipment` of the relevant :py:class:`Building`.
    :param request: The HTTP request.
    :param building_name: The name of the :py:class:`Building` the :py:class:`Equipment` belongs to.
    :return: An HTTP response containing a page with all the available equipment of the relevant :py:class:`Building`.
    """
    building = Building.objects.get(name=building_name)
    equipment_list = building.get_all_equipment()
    return render(request, "aubouleau_web/building_equipment.html", {"building": building, "equipment_list": equipment_list})
