from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        groups = [
            {'name': 'managers', 'description': 'Менеджеры'}
        ]

        for group_data in groups:
            group, created = Group.objects.get_or_create(name=group_data['name'])
            if created:
                group.description = group_data['description']
                group.save()

    permissions = [
        'users.block_user',
        'users.view_user_list',
        'service.view_all_newsletter',
        'service.deactivate_newsletter',
        'blog.delete_blog',
        'blog.change_blog',
        'blog.add_blog',
    ]
    for perm in permissions:
        app_label, codename = perm.split('.')
        permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
        group.permissions.add(permission)
