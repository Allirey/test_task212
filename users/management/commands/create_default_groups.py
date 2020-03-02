from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


PERMISSION_GROUPS = [
    ('users', []),
    ('redactors', ['publish_without_moderation']),
    ('admins', [
        'add_article', 'change_article',
        'delete_article', 'view_article',
        'add_comment', 'change_comment',
        'delete_comment', 'view_comment',
        'publish_without_moderation'
    ])
]


class Command(BaseCommand):
    help = 'Creates default groups (Users, Redactors, Admins)'

    def handle(self, *args, **options):
        for group, permissions in PERMISSION_GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for codename in permissions:
                try:
                    permission = Permission.objects.get(codename=codename)
                except Permission.DoesNotExist as e:
                    print(e, codename)
                    continue

                new_group.permissions.add(permission)