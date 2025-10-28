from django.contrib import admin
from .models import ModuloEstudio, Leccion

@admin.register(ModuloEstudio)
class ModuloEstudioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'orden', 'duracion_estimada', 'activo']
    list_filter = ['activo']
    ordering = ['orden']

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'modulo', 'orden', 'tipo_contenido']
    list_filter = ['modulo', 'tipo_contenido']
    ordering = ['modulo', 'orden']