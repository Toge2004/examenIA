from django.db import models
from django.contrib.auth.models import User

class Modulo(models.Model):
	NIVEL_CHOICES = [
		('basico', 'Básico'),
		('intermedio', 'Intermedio'),
		('avanzado', 'Avanzado'),
	]
    
	titulo = models.CharField(max_length=100)
	descripcion = models.TextField()
	nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
	duracion_estimada = models.IntegerField(help_text="Duración en minutos")
    
	def __str__(self):
		return self.titulo

class PreguntaDiagnostico(models.Model):
	modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
	texto = models.TextField()
	opcion_a = models.CharField(max_length=200)
	opcion_b = models.CharField(max_length=200)
	opcion_c = models.CharField(max_length=200)
	opcion_d = models.CharField(max_length=200)
	respuesta_correcta = models.CharField(max_length=1, choices=[
		('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
	])
    
	def __str__(self):
		return f"Pregunta para {self.modulo.titulo}"

class ResultadoDiagnostico(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
	puntaje = models.IntegerField()
	fecha = models.DateTimeField(auto_now_add=True)
	necesita_refuerzo = models.BooleanField(default=True)
    
	class Meta:
		unique_together = ['usuario', 'modulo']

class ProgresoUsuario(models.Model):
	ESTADO_CHOICES = [
		('pendiente', 'Pendiente'),
		('en_curso', 'En Curso'),
		('completado', 'Completado'),
	]

	usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progreso_capacitacion')
	modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
	estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
	fecha_inicio = models.DateTimeField(null=True, blank=True)
	fecha_completado = models.DateTimeField(null=True, blank=True)

	class Meta:
		unique_together = ['usuario', 'modulo']
