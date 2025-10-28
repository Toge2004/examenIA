from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegistroForm

def home(request):
    """Página de inicio - Redirige según autenticación"""
    if request.user.is_authenticated:
        return redirect('usuarios:dashboard_usuario')
    else:
        return redirect('login')

def registro(request):
    """Vista de registro de usuarios"""
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido/a {user.first_name or user.username}! Registro exitoso.')
            return redirect('usuarios:dashboard_usuario')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = RegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})

def custom_login(request):
    """Vista personalizada de login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido/a {user.first_name or user.username}!')
            return redirect('usuarios:dashboard_usuario')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'usuarios/login.html')

@login_required
def dashboard_usuario(request):
    """Dashboard principal del usuario"""
    # Aquí puedes agregar lógica para mostrar información del usuario
    # como progreso del diagnóstico, módulos completados, etc.
    context = {
        'user': request.user,
    }
    return render(request, 'usuarios/dashboard.html', context)

@login_required
def perfil_usuario(request):
    """Vista del perfil del usuario"""
    if request.method == 'POST':
        # Lógica para actualizar el perfil
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('usuarios:perfil_usuario')
    
    return render(request, 'usuarios/perfil.html')

@login_required
def editar_perfil(request):
    """Vista para editar el perfil del usuario"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('usuarios:perfil_usuario')
    
    return render(request, 'usuarios/editar_perfil.html')

def registro_simple(request):
    """Vista de registro alternativa usando el formulario por defecto de Django"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido/a.')
            return redirect('usuarios:dashboard_usuario')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro_simple.html', {'form': form})
