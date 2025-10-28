from django.urls import path
from . import views

app_name = 'diagnostico'

urlpatterns = [
    path('dashboard/', views.dashboard_diagnostico, name='dashboard_diagnostico'),
    path('progreso/', views.dashboard_progreso, name='dashboard_progreso'),
    path('iniciar/', views.iniciar_diagnostico, name='iniciar_diagnostico'),
    path('resultado/', views.resultado_diagnostico, name='resultado_diagnostico'),
    path('reiniciar/', views.reiniciar_diagnostico, name='reiniciar_diagnostico'),
]
