# Data migration: Create Viewers, Editors, and Admins groups with assigned permissions.
# Viewers: can_view only.
# Editors: can_view, can_create, can_edit.
# Admins: can_view, can_create, can_edit, can_delete.
# Permissions are created here so they exist before post_migrate runs.

from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_groups(apps, schema_editor):
    """Create permissions for Book (if missing), then create groups and assign permissions."""
    content_type = ContentType.objects.get(app_label='relationship_app', model='book')

    def get_or_create_perm(codename, name):
        perm, _ = Permission.objects.get_or_create(
            content_type=content_type,
            codename=codename,
            defaults={'name': name},
        )
        return perm

    perms = {
        'can_view': get_or_create_perm('can_view', 'Can view'),
        'can_create': get_or_create_perm('can_create', 'Can create'),
        'can_edit': get_or_create_perm('can_edit', 'Can edit'),
        'can_delete': get_or_create_perm('can_delete', 'Can delete'),
    }

    viewers, _ = Group.objects.get_or_create(name='Viewers')
    viewers.permissions.add(perms['can_view'])

    editors, _ = Group.objects.get_or_create(name='Editors')
    editors.permissions.add(perms['can_view'], perms['can_create'], perms['can_edit'])

    admins, _ = Group.objects.get_or_create(name='Admins')
    admins.permissions.add(perms['can_view'], perms['can_create'], perms['can_edit'], perms['can_delete'])


def remove_groups(apps, schema_editor):
    """Remove the created groups (reverse migration)."""
    Group.objects.filter(name__in=['Viewers', 'Editors', 'Admins']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0003_alter_book_permissions'),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]
