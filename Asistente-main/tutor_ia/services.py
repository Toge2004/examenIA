from .models import PreguntaFrecuente

class TutorLocal:
    def __init__(self):
        self.respuestas = self.cargar_respuestas()
        
        self.sinonimos = {
            "hi": "hola", "hello": "hola", "bye": "adiós", "thanks": "gracias",
            "help": "ayuda", "diagnostico": "diagnóstico", "python": "qué es python",
            "django": "qué es django", "html": "qué es html", "css": "qué es css",
            "javascript": "qué es javascript", "js": "qué es javascript",
        }
    
    def cargar_respuestas(self):
        """Carga respuestas desde la base de datos"""
        respuestas_base = {
            "hola": "¡Hola! Soy tu tutor de desarrollo de software. ¿En qué puedo ayudarte?",
            "adiós": "¡Hasta luego! Recuerda practicar regularmente para mejorar tus habilidades.",
            "gracias": "¡De nada! Estoy aquí para ayudarte en tu aprendizaje.",
            "ayuda": "Puedo ayudarte con: \n• Preguntas sobre diagnóstico \n• Conceptos de programación \n• Uso de la plataforma \n• Django y Python",
        }
        
        try:
            preguntas_db = PreguntaFrecuente.objects.filter(activa=True)
            for pregunta in preguntas_db:
                respuestas_base[pregunta.pregunta.lower()] = pregunta.respuesta
        except:
            pass
            
        return respuestas_base
    
    def limpiar_texto(self, texto):
        """Limpia y normaliza el texto"""
        import re
        texto = texto.lower().strip()
        texto = re.sub(r'[^\w\sáéíóúñ]', '', texto)  
        texto = re.sub(r'\s+', ' ', texto)
        return texto
    
    def encontrar_respuesta(self, pregunta):
        pregunta_limpia = self.limpiar_texto(pregunta)
        
        if pregunta_limpia in self.sinonimos:
            pregunta_limpia = self.sinonimos[pregunta_limpia]
        
        if pregunta_limpia in self.respuestas:
            return self.respuestas[pregunta_limpia]
        
        palabras = pregunta_limpia.split()
        for palabra in palabras:
            if palabra in self.respuestas:
                return self.respuestas[palabra]
        
        for key in self.respuestas.keys():
            if key in pregunta_limpia:
                return self.respuestas[key]
        
        return "Lo siento, no tengo información sobre eso. Puedo ayudarte con: diagnóstico, Python, Django, HTML, CSS, JavaScript o el uso de la plataforma."