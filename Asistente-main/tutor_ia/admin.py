from django.contrib import admin
from .models import PreguntaFrecuente, Conversacion, Mensaje

@admin.register(PreguntaFrecuente)
class PreguntaFrecuenteAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'categoria', 'activa', 'fecha_creacion')
    list_filter = ('categoria', 'activa')
    search_fields = ('pregunta', 'respuesta')
    list_editable = ('activa',)

@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('usuario__username', 'titulo')

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversacion', 'es_usuario', 'fecha_creacion')
    list_filter = ('es_usuario', 'fecha_creacion')
    
    def contenido_truncado(self, obj):
        return obj.contenido[:50] + '...' if len(obj.contenido) > 50 else obj.contenido
    contenido_truncado.short_description = 'Contenido'