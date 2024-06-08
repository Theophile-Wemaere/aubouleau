from django.contrib.auth.models import Group, User

admin_user = User.objects.get(pk=1)
if not Group.objects.get(name="Administrators").user_set.contains(admin_user):
    Group.objects.get(name="Administrators").user_set.add(admin_user)
    print(f'Added user "{admin_user.username}" to the "Administrators" group.')
else:
    print(f'Skip adding user "{admin_user.username}" to the "Administrators" group (user already in group).')
