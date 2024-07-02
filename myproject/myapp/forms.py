from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Residente, Aportador, Aporte, Insumo
from datetime import date
import re


class ResidenteForm(forms.ModelForm):
    class Meta:
        model = Residente
        fields = ['nombre', 'edad', 'estado_salud', 'fecha_ingreso']

class RegistroAportadorForm(UserCreationForm):
    class Meta:
        model = Aportador
        fields = ['rut', 'first_name', 'last_name', 'email', 'fecha_nacimiento', 'telefono', 'direccion', 'region', 'comuna']

    class Meta:
        model = Aportador
        fields = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'telefono', 'email', 'direccion', 'region', 'comuna']

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if Aportador.objects.filter(rut=rut).exists():
            raise forms.ValidationError('El RUT ya está registrado.')
        return rut

    def validar_rut(self, rutCompleto):
        rutCompleto = rutCompleto.replace("‐","-")
        if not re.match(r'^[0-9]+-[0-9kK]{1}$', rutCompleto):
            return False
        rut, dv = rutCompleto.split('-')
        if dv == 'K':
            dv = 'k'
        return self.dv(int(rut)) == dv

    def dv(self, T):
        M=0
        S=1
        while T:
            S=(S+T%10*(9-M%6))%11
            M+=1
            T//=10
        return str(S-1) if S else 'k'

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get("fecha_nacimiento")
        edad = (date.today() - fecha_nacimiento).days / 365.25
        if edad < 18:
            raise forms.ValidationError("Debe ser mayor de 18 años.")
        return fecha_nacimiento

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        if not re.match(r"^\d{9}$", telefono):
            raise forms.ValidationError("El teléfono debe tener 9 dígitos.")
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Aportador.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo electrónico ya está registrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get("rut")
        if Aportador.objects.filter(rut=rut).exists():
            self.add_error("rut", "El RUT ya está registrado")
        email = cleaned_data.get("email")
        if Aportador.objects.filter(email=email).exists():
            self.add_error("email", "El email ya está registrado")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            self.add_error("password_confirm", "Las contraseñas no coinciden")


        return cleaned_data
    
class AporteForm(forms.ModelForm):
    TIPO_APORTE_CHOICES = [
        ('', 'Seleccione'),
        ('credito', 'Tarjeta de Crédito'),
        ('transferencia', 'Transferencia Bancaria'),
    ]
    tipo_aporte = forms.ChoiceField(choices=TIPO_APORTE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    numero_tarjeta = forms.CharField(max_length=12, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre_titular = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha_vencimiento = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/AA'}))
    cvv = forms.CharField(max_length=3, required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    comprobante = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Aporte
        fields = ['monto', 'comentario']

    def clean_numero_tarjeta(self):
        numero_tarjeta = self.cleaned_data.get('numero_tarjeta')
        if numero_tarjeta and len(numero_tarjeta) != 12:
            raise forms.ValidationError("El número de tarjeta debe tener 12 dígitos.")
        return numero_tarjeta

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        if fecha_vencimiento:
            if not re.match(r'(0[1-9]|1[0-2])\/[0-9]{2}$', fecha_vencimiento):
                raise forms.ValidationError("La fecha de vencimiento debe estar en el formato MM/AA.")
        return fecha_vencimiento

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if cvv and len(cvv) != 3:
            raise forms.ValidationError("El CVV debe tener 3 dígitos.")
        return cvv
    

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))


class RegistroRecepcionForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'cantidad', 'fecha_recepcion']