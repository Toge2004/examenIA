from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('dashboard/', views.dashboard_usuario, name='dashboard_usuario'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]