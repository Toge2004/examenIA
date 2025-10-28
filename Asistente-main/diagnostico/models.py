from django.db import models
from django.contrib.auth.models import User

class Modulo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    texto = models.TextField()
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.modulo.nombre} - Pregunta {self.orden}"

class OpcionRespuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)
    valor = models.IntegerField()  
    es_correcta = models.BooleanField(default=False)
    
    def __str__(self):
        return self.texto

class DiagnosticoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    completado = models.BooleanField(default=False)

    class Meta:
        db_table = 'diagnostico_diagnostico'

    def __str__(self):
        return f"Diagnóstico de {self.usuario.username}"

class RespuestaUsuario(models.Model):
    diagnostico = models.ForeignKey(DiagnosticoUsuario, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(OpcionRespuesta, on_delete=models.CASCADE)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'diagnostico_respuestadiagnostico'

