from django.contrib import admin
from .models import Modulo, PreguntaDiagnostico, ResultadoDiagnostico, ProgresoUsuario

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'nivel', 'duracion_estimada']

@admin.register(PreguntaDiagnostico)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['modulo', 'texto', 'respuesta_correcta']

@admin.register(ResultadoDiagnostico)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'modulo', 'puntaje', 'necesita_refuerzo']

@admin.register(ProgresoUsuario)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'modulo', 'estado']