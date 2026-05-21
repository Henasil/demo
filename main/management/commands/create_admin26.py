from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from main.models import UserProfile


class Command(BaseCommand):
    help = 'Создает демонстрационного администратора Admin26 с паролем Demo20'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username='Admin26')
        user.set_password('Demo20')
        user.email = 'admin26@passazhiry.local'
        user.is_staff = True
        user.is_superuser = True
        user.save()

        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'full_name': 'Администратор портала Пассажиры РФ',
                'phone': '+7 (000) 000-00-00',
                'email': user.email,
            },
        )

        action = 'создан' if created else 'обновлен'
        self.stdout.write(self.style.SUCCESS(f'Администратор Admin26 {action}. Пароль: Demo20'))
