import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Aportador

def create_colaborator(email, password, first_name, last_name, **extra_fields):
    user = Aportador.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_colaborador=True,
        **extra_fields
    )
    user.save()
    print(f'Colaborador {email} creado con éxito.')

if __name__ == '__main__':
    create_colaborator(
        email='admin@care.cl',
        password='123',
        first_name='admin',
        last_name='admin',
        fecha_nacimiento='1980-01-01',
        telefono='123456789',
        direccion='Calle Falsa 123',
        region='Metropolitana',
        comuna='Santiago'
    )
