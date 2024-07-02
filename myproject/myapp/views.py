from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroAportadorForm, ResidenteForm, AporteForm, LoginForm, RegistroRecepcionForm
from .models import Residente, Aportador, Insumo
from django.http import JsonResponse

def home(request):
    return render(request, 'myapp/home.html')

def farmacia(request):
    return render(request, 'myapp/farmacia.html')

def farmacia_busqueda(request):
    return render(request, 'myapp/farmacia_busqueda.html')


def farmacia_entrega_insumos(request):
    return render(request, 'myapp/farmacia_entrega_insumos.html')



def asistencia(request):
    return render(request, 'myapp/asistencia.html')

def ayuda(request):
    return render(request, 'myapp/ayuda.html')

def configuracion(request):
    return render(request, 'myapp/configuracion.html')

def ingresos(request):
    return render(request, 'myapp/ingresos.html')

def reportes(request):
    return render(request, 'myapp/reportes.html')

def login_colaboradores(request):
    if request.method == 'POST':
        # Lógica de autenticación de colaboradores
        pass
    return render(request, 'myapp/login_colaboradores.html')

def residentes(request):
    residentes = Residente.objects.all()
    return render(request, 'myapp/residentes.html', {'residentes': residentes})

def agregar_residente(request):
    if request.method == "POST":
        form = ResidenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('residentes')
    else:
        form = ResidenteForm()
    return render(request, 'agregar_residente.html', {'form': form})

def editar_residente(request, id):
    residente = get_object_or_404(Residente, id=id)
    if request.method == 'POST':
        form = ResidenteForm(request.POST, instance=residente)
        if form.is_valid():
            form.save()
            return redirect('residentes')
    else:
        form = ResidenteForm(instance=residente)
    return render(request, 'myapp/editar_residente.html', {'form': form})

def eliminar_residente(request, id):
    residente = get_object_or_404(Residente, id=id)
    if request.method == 'POST':
        residente.delete()
        return redirect('residentes')
    return render(request, 'myapp/eliminar_residente.html', {'residente': residente})

def registro_aportadores(request):
    if request.method == 'POST':
        form = RegistroAportadorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registro exitoso. Ahora puede iniciar sesión.')
            return redirect('login_aportadores')
    else:
        form = RegistroAportadorForm()
    return render(request, 'myapp/registro_aportadores.html', {'form': form})

from django.http import JsonResponse

def validar_rut(request):
    rut = request.GET.get('rut', None)
    data = {
        'is_taken': Aportador.objects.filter(rut=rut).exists()
    }
    return JsonResponse(data)

def validar_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': Aportador.objects.filter(email=email).exists()
    }
    return JsonResponse(data)

def login_aportadores(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_aportador:
            login(request, user)
            return redirect('index2')
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
    return render(request, 'myapp/login_aportadores.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def index2(request):
    return render(request, 'myapp/index.html')

def aportar(request):
    if request.method == 'POST':
        # Lógica para procesar un aporte
        pass
    return render(request, 'aportar.html')


def mis_aportes(request):
    # Lógica para mostrar los aportes del usuario
    return render(request, 'mis_aportes.html')

@login_required
def aportar(request):
    if request.method == 'POST':
        form = AporteForm(request.POST, request.FILES)
        if form.is_valid():
            aporte = form.save(commit=False)
            aporte.aportador = request.user  # Asegurarse de que se asigna el usuario actual
            aporte.save()
            messages.success(request, f"Gracias por su aporte de ${aporte.monto}.")
            return redirect('index2')  # Redirigir a la vista de index2
    else:
        form = AporteForm()
    return render(request, 'myapp/aportar.html', {'form': form})

def login_colaboradores(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'myapp/login_colaboradores.html', {'form': form})

def index(request):
    return render(request, 'myapp/index.html')

def farmacia_registrar_recepcion(request):
    if request.method == 'POST':
        form = RegistroRecepcionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmacia_registrar_recepcion')  # Redirige a la misma página después de guardar
    else:
        form = RegistroRecepcionForm()
    
    insumos = Insumo.objects.all()
    return render(request, 'myapp/farmacia_registrar_recepcion.html', {'form': form, 'insumos': insumos})

def farmacia_inventario(request):
    insumos = Insumo.objects.all()
    return render(request, 'myapp/farmacia_inventario.html', {'insumos': insumos})