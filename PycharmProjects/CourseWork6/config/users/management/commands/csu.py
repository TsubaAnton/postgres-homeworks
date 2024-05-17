from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        email = 'ontontsuba@icloud.com'
        password = 'Onton1010'  # Замените на желаемый пароль
        if not User.objects.filter(email=email).exists():
            user = User.objects.create(email=email)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
