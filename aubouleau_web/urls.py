from django.urls import path

from . import views

app_name = 'aubouleau_web'
# Note: all URLs are relative to the root URL declared in ../aubouleau/urls.py
urlpatterns = [
    # /
    # Example: https://aubouleau.fr/
    path("", views.index, name="index"),

    # /login
    # Example: https://aubouleau.fr/login
    path("login/", views.sign_in, name="sign_in"),
    # /register
    # Example: https://aubouleau.fr/register
    path("register/", views.sign_up, name="sign_up"),
    # /logout
    # Example: https://aubouleau.fr/logout
    path("logout/", views.sign_out, name="sign_out"),
    # /profile
    # Example: https://aubouleau.fr/profile
    path("profile/", views.profile, name="profile"),

    # /search
    # Example: https://aubouleau.fr/search
    path("search/", views.search, name="search"),

    # /administration/buildings
    # Example: https://aubouleau.fr/administration/buildings
    path("administration/buildings/", views.administration_buildings, name="administration_buildings"),
    # /administration/buildings/new
    # Example: https://aubouleau.fr/administration/buildings/new
    path("administration/buildings/new", views.administration_buildings_new, name="administration_buildings_new"),
    # /administration/buildings/edit/[building_name]
    # Example: https://aubouleau.fr/administration/buildings/edit/NDL
    path("administration/buildings/edit/<str:building_name>/", views.administration_buildings_edit, name="administration_buildings_edit"),
    # /administration/buildings/delete/[building_name]
    # Example: https://aubouleau.fr/administration/buildings/delete/NDL
    path("administration/buildings/delete/<str:building_name>/", views.administration_buildings_delete, name="administration_buildings_delete"),

    # /administration/floors
    # Example: https://aubouleau.fr/administration/floors
    path("administration/floors/", views.administration_floors, name="administration_floors"),
    # /administration/floors/new
    # Example: https://aubouleau.fr/administration/floors/new
    path("administration/floors/new", views.administration_floors_new, name="administration_floors_new"),
    # /administration/floors/edit/[building_name/[floor_number]
    # Example: https://aubouleau.fr/administration/floors/edit/NDL/0
    path("administration/floors/edit/<str:building_name>/<int:floor_number>/", views.administration_floors_edit, name="administration_floors_edit"),
    # /administration/floors/delete/[building_name]/[floor_number]
    # Example: https://aubouleau.fr/administration/floors/delete/NDL/0
    path("administration/floors/delete/<str:building_name>/<int:floor_number>/", views.administration_floors_delete, name="administration_floors_delete"),

    # /administration/rooms
    # Example: https://aubouleau.fr/administration/rooms
    path("administration/rooms/", views.administration_rooms, name="administration_rooms"),
    # /administration/rooms/new
    # Example: https://aubouleau.fr/administration/rooms/new
    path("administration/rooms/new", views.administration_rooms_new, name="administration_rooms_new"),
    # /administration/rooms/edit/[room_number]
    # Example: https://aubouleau.fr/administration/rooms/edit/L012
    path("administration/rooms/edit/<str:room_number>/", views.administration_rooms_edit, name="administration_rooms_edit"),
    # /administration/rooms/delete/[room_number]
    # Example: https://aubouleau.fr/administration/rooms/delete/L012
    path("administration/rooms/delete/<str:room_number>/", views.administration_rooms_delete, name="administration_rooms_delete"),

    # /administration/equipment
    # Example: https://aubouleau.fr/administration/equipment
    path("administration/equipment/", views.administration_equipment, name="administration_equipment"),
    # /administration/equipment/new
    # Example: https://aubouleau.fr/administration/equipment/new
    path("administration/equipment/new", views.administration_equipment_new, name="administration_equipment_new"),
    # /administration/equipment/edit/[equipment_id]
    # Example: https://aubouleau.fr/administration/equipment/edit/1
    path("administration/equipment/edit/<int:equipment_id>/", views.administration_equipment_edit, name="administration_equipment_edit"),
    # /administration/equipment/delete/[equipment_id]
    # Example: https://aubouleau.fr/administration/equipment/delete/1
    path("administration/equipment/delete/<int:equipment_id>/", views.administration_equipment_delete, name="administration_equipment_delete"),

    # /administration/equipment_types
    # Example: https://aubouleau.fr/administration/equipment_types
    path("administration/equipment_types/", views.administration_equipment_types, name="administration_equipment_types"),
    # /administration/equipment_types/new
    # Example: https://aubouleau.fr/administration/equipment_types/new
    path("administration/equipment_types/new", views.administration_equipment_types_new, name="administration_equipment_types_new"),
    # /administration/equipment_types/edit/[equipment_type_name]
    # Example: https://aubouleau.fr/administration/equipment_types/edit/Computers
    path("administration/equipment/edit/<str:equipment_type_name>/", views.administration_equipment_types_edit, name="administration_equipment_types_edit"),
    # /administration/equipment_types/delete/[equipment_type_name]
    # Example: https://aubouleau.fr/administration/equipment_types/delete/Computers
    path("administration/equipment_types/delete/<str:equipment_type_name>/", views.administration_equipment_types_delete, name="administration_equipment_types_delete"),

    # /equipment/[equipment_type]
    # Example: https://aubouleau.fr/equipment/computers
    path("equipment/<str:equipment_type_name>/", views.equipment, name="equipment"),

    # /problems
    # Example: https://aubouleau.fr/problems
    path("problems/", views.problems, name="problems"),
    # /problems/closed
    # Example: https://aubouleau.fr/problems/closed
    path("problems/closed/", views.problems_closed, name="problems_closed"),
    # /problems/[problem_id]
    # Example: https://aubouleau.fr/problems/0
    path("problems/<int:problem_id>/", views.problem_detail, name="problem_detail"),
    # /problems/new
    # Example: https://aubouleau.fr/problems/new
    path("problems/new/", views.problems_new, name="problems_new"),
    # /problems/solve/[problem_id]
    # Example: https://aubouleau.fr/solve/delete/0
    path("problems/solve/<int:problem_id>/", views.problems_solve, name="problems_solve"),
    # /problems/close/[problem_id]
    # Example: https://aubouleau.fr/close/delete/0
    path("problems/close/<int:problem_id>/", views.problems_close, name="problems_close"),
    # /problems/delete/[problem_id]
    # Example: https://aubouleau.fr/problems/delete/0
    path("problems/delete/<int:problem_id>/", views.problems_delete, name="problems_delete"),
    # /problems/[problem_id]/comment/add
    # Example: https://aubouleau.fr/problems/0/comment/add
    path("problems/<int:problem_id>/comment/add/", views.problems_comment_add, name="problem_comment_add"),
    # /problems/[problem_id]/comment/delete/[comment_id]
    # Example: https://aubouleau.fr/problems/0/comment/delete/0
    path("problems/<int:problem_id>/comment/delete/<int:comment_id>/", views.problems_comment_delete, name="problem_comment_delete"),


    # /buildings
    # Example: https://aubouleau.fr/buildings
    path("buildings/", views.buildings, name="buildings"),
    # /[building_name]
    # Example: https://aubouleau.fr/NDL
    path("<str:building_name>/", views.building_detail, name="building_detail"),
    # /[building_name]/floors
    # Example: https://aubouleau.fr/NDL/floors
    path("<str:building_name>/floors/", views.building_floors, name="building_floors"),
    # /[building_name]/floors/[floor_number]
    # Example: https://aubouleau.fr/NDL/floors/0
    path("<str:building_name>/floors/<int:floor_number>/", views.floor_detail, name="floor_detail"),
    # /[building_name]/floors/[floor_number]/rooms
    # Example: https://aubouleau.fr/NDL/floors/0/rooms
    path("<str:building_name>/floors/<int:floor_number>/rooms/", views.floor_rooms, name="floor_rooms"),
    # /[building_name]/floors/[floor_number]/equipment
    # Example: https://aubouleau.fr/NDL/floors/1/equipment
path("<str:building_name>/floors/<int:floor_number>/equipment/", views.floor_equipment, name="floor_equipment"),
    # /[building_name]/rooms
    # Example: https://aubouleau.fr/NDL/rooms
    path("<str:building_name>/rooms/", views.building_rooms, name="building_rooms"),
    # /[building_name]/rooms/[room_number]
    # Example: https://aubouleau.fr/NDL/rooms/L012
    path("<str:building_name>/rooms/<str:room_number>/", views.room_detail, name="room-detail"),
    # /[building_name]/equipment
    # Example: https://aubouleau.fr/NDL/equipment
    path("<str:building_name>/equipment/", views.building_equipment, name="building_equipment"),
]
