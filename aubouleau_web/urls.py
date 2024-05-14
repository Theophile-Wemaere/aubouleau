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
    # /[building_id]
    # Example: https://aubouleau.fr/ndc
    path("<int:building_id>/", views.building_detail, name="building_detail"),
    # /[building_id]/floors
    # Example: https://aubouleau.fr/ndc/floors
    path("<int:building_id>/floors/", views.floors, name="floors"),
    # /[building_id]/floors/[floor_id]
    # Example: https://aubouleau.fr/ndc/floors/0
    path("<int:building_id>/floors/<int:floor_id>/", views.floor_detail, name="floor_detail"),
    # /[building_id]/rooms
    # Example: https://aubouleau.fr/ndc/rooms
    path("<int:building_id>/rooms/", views.rooms, name="rooms"),
    # /[building_id]/rooms/[room_id]
    # Example: https://aubouleau.fr/ndc/rooms/l012
    path("<int:building_id>/rooms/<int:room_id>/", views.room_detail, name="room-detail"),
]
