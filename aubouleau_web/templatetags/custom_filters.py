from django import template

register = template.Library()


# Custom DTL filter that returns True if the user belongs to the "Administrators" group
@register.filter(name='is_administrator')
def is_administrator(user):
    return user.groups.filter(name='Administrators').exists()
