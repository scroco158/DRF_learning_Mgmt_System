from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        user = User.objects.create(email='admin@admin.ru')

        user.set_password('admin')
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()