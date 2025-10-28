from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json

class TutorIAView(View):
    def get(self, request):
        return render(request, 'tutor_ia/chat.html')
    
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje', '').strip().lower()
            
            if not mensaje:
                return JsonResponse({'success': False, 'error': 'Mensaje vacío'})
            
            respuesta = self.obtener_respuesta(mensaje)
            
            return JsonResponse({
                'success': True, 
                'respuesta': respuesta
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    def obtener_respuesta(self, mensaje):
        faqs = {
            
            'diagnóstico': "🔍 **Sistema de Diagnóstico**\n\nEl diagnóstico evalúa tus conocimientos en Python, Django, HTML, CSS y JavaScript. Consiste en preguntas de múltiple opción que te ayudarán a identificar tu nivel actual.",
            'diagnostico': "🔍 **Sistema de Diagnóstico**\n\nEl diagnóstico evalúa tus conocimientos en Python, Django, HTML, CSS y JavaScript. Consiste en preguntas de múltiple opción que te ayudarán a identificar tu nivel actual.",
            'evaluación': "🔍 **Sistema de Diagnóstico**\n\nEl diagnóstico evalúa tus conocimientos en Python, Django, HTML, CSS y JavaScript. Consiste en preguntas de múltiple opción que te ayudarán a identificar tu nivel actual.",
            'test': "🔍 **Sistema de Diagnóstico**\n\nEl diagnóstico evalúa tus conocimientos en Python, Django, HTML, CSS y JavaScript. Consiste en preguntas de múltiple opción que te ayudarán a identificar tu nivel actual.",
            
            
            'python': "🐍 **Python**\n\nPython es un lenguaje de programación fácil de aprender, ideal para principiantes. Se usa para desarrollo web, análisis de datos, inteligencia artificial y más.",
            'qué es python': "🐍 **Python**\n\nPython es un lenguaje de programación interpretado de alto nivel. Su sintaxis clara lo hace perfecto para empezar en programación.",
            'que es python': "🐍 **Python**\n\nPython es un lenguaje de programación interpretado de alto nivel. Su sintaxis clara lo hace perfecto para empezar en programación.",
            
            'django': "🎸 **Django**\n\nDjango es un framework web de Python que facilita la creación de aplicaciones web robustas y seguras. Incluye ORM, panel de administración y autenticación.",
            'qué es django': "🎸 **Django**\n\nDjango es un framework web que sigue el patrón MVT (Modelo-Vista-Template). Es ideal para desarrollar aplicaciones web complejas rápidamente.",
            'que es django': "🎸 **Django**\n\nDjango es un framework web que sigue el patrón MVT (Modelo-Vista-Template). Es ideal para desarrollar aplicaciones web complejas rápidamente.",
            
            'html': "🌐 **HTML**\n\nHTML es el lenguaje estándar para crear páginas web. Define la estructura y el contenido usando etiquetas como <h1>, <p>, <div>.",
            'css': "🎨 **CSS**\n\nCSS se usa para dar estilo a las páginas web. Controla colores, fuentes, diseños y la apariencia general del sitio.",
            'javascript': "⚡ **JavaScript**\n\nJavaScript hace que las páginas web sean interactivas. Se ejecuta en el navegador y permite crear efectos, validar formularios y más.",
            
            'plataforma': "🖥️ **Plataforma**\n\nNuestra plataforma ofrece diagnóstico inicial, contenido personalizado y seguimiento de progreso. Comienza con el diagnóstico para obtener recomendaciones.",
            'cómo usar': "🖥️ **Uso de la Plataforma**\n\n1. Realiza el diagnóstico inicial\n2. Revisa tus resultados\n3. Accede al contenido recomendado\n4. Practica con ejercicios",
            'como usar': "🖥️ **Uso de la Plataforma**\n\n1. Realiza el diagnóstico inicial\n2. Revisa tus resultados\n3. Accede al contenido recomendado\n4. Practica con ejercicios",
            
            'ayuda': "🤖 **Asistente Virtual**\n\nPuedo ayudarte con:\n• Información sobre el diagnóstico\n• Explicaciones de Python, Django\n• Conceptos de HTML, CSS, JavaScript\n• Uso de la plataforma\n\nUsa los botones de preguntas rápidas o escribe tu duda.",
            'help': "🤖 **Asistente Virtual**\n\nPuedo ayudarte con:\n• Información sobre el diagnóstico\n• Explicaciones de Python, Django\n• Conceptos de HTML, CSS, JavaScript\n• Uso de la plataforma\n\nUsa los botones de preguntas rápidas o escribe tu duda.",
        }
        
        if mensaje in faqs:
            return faqs[mensaje]
        
        for palabra_clave, respuesta in faqs.items():
            if palabra_clave in mensaje:
                return respuesta
        
        return "❓ **Pregunta no reconocida**\n\nNo encuentro una respuesta para tu pregunta. Puedo ayudarte con:\n\n• **Diagnóstico del sistema**\n• **Python y Django**\n• **HTML, CSS, JavaScript**\n• **Uso de la plataforma**\n\nUsa los botones de preguntas rápidas o intenta con términos más específicos."