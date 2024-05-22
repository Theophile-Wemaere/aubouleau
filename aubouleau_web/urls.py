from django.urls import path

from . import views

app_name = 'aubouleau_web'
# Note: all URLs are relative to the root URL declared in ../aubouleau/urls.py
urlpatterns = [
    # /
    # Example: https://aubouleau.fr/
    path("", views.index, name="index"),
    # /buildings
    # Example: https://aubouleau.fr/buildings
    path("buildings/", views.buildings, name="buildings"),
    # /[building_name]
    # Example: https://aubouleau.fr/NDC
    path("<str:building_name>/", views.building_detail, name="building_detail"),
    # /[building_name]/floors
    # Example: https://aubouleau.fr/NDC/floors
    path("<str:building_name>/floors/", views.floors, name="floors"),
    # /[building_name]/floors/[floor_number]
    # Example: https://aubouleau.fr/NDC/floors/0
    path("<str:building_name>/floors/<int:floor_number>/", views.floor_detail, name="floor_detail"),
    # /[building_name]/rooms
    # Example: https://aubouleau.fr/NDC/rooms
    path("<str:building_name>/rooms/", views.rooms, name="rooms"),
    # /[building_name]/rooms/[room_number]
    # Example: https://aubouleau.fr/NDC/rooms/L012
    path("<str:building_name>/rooms/<str:room_number>/", views.room_detail, name="room-detail"),
]
