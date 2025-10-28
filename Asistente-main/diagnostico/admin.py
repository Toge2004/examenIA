
from django.contrib import admin
from .models import Modulo, Pregunta, OpcionRespuesta, DiagnosticoUsuario, RespuestaUsuario

admin.site.register(Modulo)
admin.site.register(Pregunta)
admin.site.register(OpcionRespuesta)
admin.site.register(DiagnosticoUsuario)
admin.site.register(RespuestaUsuario)

def crear_preguntas_ejemplo():
	modulo, _ = Modulo.objects.get_or_create(nombre="Competencias Digitales", descripcion="Diagnóstico breve")
	textos = [
		"¿Con qué frecuencia usas herramientas ofimáticas (Word, Excel, etc.)?",
		"¿Te sientes cómodo navegando y buscando información en Internet?",
		"¿Has utilizado plataformas de aprendizaje en línea?",
		"¿Sabes cómo proteger tus datos personales en la web?",
		"¿Puedes identificar noticias falsas o desinformación en redes sociales?"
	]
	for i, texto in enumerate(textos, start=1):
		pregunta, _ = Pregunta.objects.get_or_create(modulo=modulo, texto=texto, orden=i)
		opciones = [
			("Nunca", 1),
			("Rara vez", 2),
			("A veces", 3),
			("Frecuentemente", 4),
			("Siempre", 5)
		]
		for opcion_texto, valor in opciones:
			OpcionRespuesta.objects.get_or_create(pregunta=pregunta, texto=opcion_texto, valor=valor)
	print("Preguntas y opciones de ejemplo creadas.")
