from .models import Building, Floor, Room


def add_sidebar_context(request):
    """
    Adds to the context of all templates the three following attributes:
        - "sidebar_buildings", which contains a list of all the Buildings
        - "sidebar_floors", which contains a list of all the Floors
        - "sidebar_rooms", which contains a list of all the Rooms
    """
    return {
        "sidebar_buildings": Building.objects.all(),
        "sidebar_floors": Floor.objects.all(),
        "sidebar_rooms": Room.objects.all(),
    }
