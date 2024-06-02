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
    # /buildings
    # Example: https://aubouleau.fr/buildings
    path("buildings/", views.buildings, name="buildings"),
    # /[building_name]
    # Example: https://aubouleau.fr/NDC
    path("<str:building_name>/", views.building_detail, name="building_detail"),
    # /[building_name]/floors
    # Example: https://aubouleau.fr/NDC/floors
    path("<str:building_name>/floors/", views.building_floors, name="building_floors"),
    # /[building_name]/floors/[floor_number]
    # Example: https://aubouleau.fr/NDC/floors/0
    path("<str:building_name>/floors/<int:floor_number>/", views.floor_detail, name="floor_detail"),
    # /[building_name]/floors/[floor_number]/rooms
    # Example: https://aubouleau.fr/NDC/floors/0/rooms
    path("<str:building_name>/floors/<int:floor_number>/rooms/", views.floor_rooms, name="floor_rooms"),
    # /[building_name]/rooms
    # Example: https://aubouleau.fr/NDC/rooms
    path("<str:building_name>/rooms/", views.building_rooms, name="building_rooms"),
    # /[building_name]/rooms/[room_number]
    # Example: https://aubouleau.fr/NDC/rooms/L012
    path("<str:building_name>/rooms/<str:room_number>/", views.room_detail, name="room-detail"),
]
