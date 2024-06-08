from django import template

from aubouleau_web.models import Problem

register = template.Library()


# Custom DTL filter that returns True if the user belongs to the "Administrators" group
@register.filter(name='is_administrator')
def is_administrator(user):
    return user.groups.filter(name='Administrators').exists()


# Custom DTL filter that returns the elapsed time since creation of a Problem (long string version)
@register.filter(name='time_elapsed_since_creation')
def time_elapsed_since_creation(problem: Problem):
    return problem.get_time_elapsed_since_creation(short=False)
