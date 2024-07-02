from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Residente(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    estado_salud = models.CharField(max_length=100, default='Saludable')  # Define un valor predeterminado
    fecha_ingreso = models.DateField(default='2023-01-01')  # Define un valor predeterminado

    def __str__(self):
        return self.nombre

class AportadorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Aportador(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=12, unique=True)
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    comuna = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_colaborador = models.BooleanField(default=False)

    objects = AportadorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'telefono', 'direccion', 'region', 'comuna']

    def __str__(self):
        return self.email

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True


class Aporte(models.Model):
    aportador = models.ForeignKey(Aportador, on_delete=models.CASCADE, related_name='aportes')
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.aportador.username} - {self.monto}"
    
class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    fecha_recepcion = models.DateField()

    def __str__(self):
        return self.nombre