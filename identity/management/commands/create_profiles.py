from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from identity.models import ProfileAdditionalInfo



class Command(BaseCommand):
    help = 'Creates profiles for existing users that do not have one'

    def handle(self, *args, **options):
        
        # Obtén todos los usuarios
        users = User.objects.all()

        # Para cada usuario
        for user in users:
            # Si el usuario no tiene un perfil
            if not ProfileAdditionalInfo.objects.filter(user=user).exists():
                # Crea un perfil para el usuario
                ProfileAdditionalInfo.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS('Successfully created profiles for existing users'))