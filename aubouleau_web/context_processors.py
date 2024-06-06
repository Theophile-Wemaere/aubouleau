from .models import Building, Floor, Room, Problem


def add_sidebar_context(request):
    """
    Adds lists containing all Buildings, Floors and Rooms to the context of all templates.
    :param request: The HTTP request.
    :return: A dictionary containing all the context variables required by the sidebar.
    """
    return {
        "sidebar_buildings": Building.objects.all(),
        "sidebar_floors": Floor.objects.all(),
        "sidebar_rooms": Room.objects.all(),
        "open_problems_count": Problem.objects.filter(status='OPEN').count()
    }
