from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def add_to_users_group(sender, instance, created, **kwargs):
    if not instance.is_superuser and created:
        try:
            instance.groups.add(Group.objects.get(name='users'))
        except Group.DoesNotExist as e:
            print(e)
