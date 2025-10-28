from django.apps import AppConfig
from django.db import transaction


class ModulosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modulos'

    def ready(self):
        pass

    @transaction.atomic
    def crear_modulos_iniciales(self):
        from .models import ModuloEstudio, Leccion
        modulos_data = [
            {
                'titulo': 'Fundamentos de la Informática',
                'descripcion': 'Introducción a los conceptos básicos de la informática, hardware, software y sistemas operativos.',
                'orden': 1,
                'duracion_estimada': 60,
                'lecciones': [
                    {'titulo': '¿Qué es la Informática?', 'contenido': 'La informática es la ciencia que estudia el tratamiento automático de la información mediante computadoras. Incluye el estudio de algoritmos, lenguajes de programación y sistemas informáticos.', 'orden': 1, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Componentes de una Computadora', 'contenido': 'Una computadora típica consta de: CPU (unidad central de procesamiento), memoria RAM, disco duro, tarjeta gráfica, placa madre y periféricos como teclado y mouse.', 'orden': 2, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Sistemas Operativos', 'contenido': 'Los sistemas operativos gestionan los recursos del hardware y proporcionan una interfaz para que los usuarios interactúen con la computadora. Ejemplos: Windows, macOS, Linux.', 'orden': 3, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Ejercicio: Identificando Componentes', 'contenido': 'Identifica los componentes principales de una computadora en una imagen o diagrama proporcionado.', 'orden': 4, 'tipo_contenido': 'ejercicio'},
                ]
            },
            {
                'titulo': 'Comunicación Digital',
                'descripcion': 'Aprende sobre comunicación efectiva en entornos digitales, incluyendo correo electrónico, redes sociales y herramientas colaborativas.',
                'orden': 2,
                'duracion_estimada': 45,
                'lecciones': [
                    {'titulo': 'Principios de Comunicación Digital', 'contenido': 'La comunicación digital requiere claridad, brevedad y respeto. Considera el contexto, la audiencia y el medio utilizado.', 'orden': 1, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Correo Electrónico Profesional', 'contenido': 'El correo electrónico es una herramienta fundamental. Aprende a redactar asuntos claros, saludos apropiados y cierres profesionales.', 'orden': 2, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Redes Sociales y Colaboración', 'contenido': 'Las redes sociales facilitan la colaboración, pero requieren moderación. Comparte contenido relevante y mantén la privacidad.', 'orden': 3, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Ejercicio: Redactando un Email', 'contenido': 'Practica redactando un correo electrónico profesional solicitando información sobre un proyecto.', 'orden': 4, 'tipo_contenido': 'ejercicio'},
                ]
            },
            {
                'titulo': 'Creación de Contenido Digital',
                'descripcion': 'Descubre cómo crear contenido atractivo para la web, incluyendo texto, imágenes y multimedia.',
                'orden': 3,
                'duracion_estimada': 50,
                'lecciones': [
                    {'titulo': 'Estructura de Contenido Web', 'contenido': 'Un buen contenido web tiene una introducción atractiva, desarrollo coherente y conclusión clara. Incluye elementos visuales para mantener el interés.', 'orden': 1, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Herramientas de Edición', 'contenido': 'Existen muchas herramientas gratuitas para editar imágenes y videos: GIMP, Inkscape, DaVinci Resolve, entre otras.', 'orden': 2, 'tipo_contenido': 'teoria'},
                    {'titulo': 'SEO y Visibilidad', 'contenido': 'El SEO (Search Engine Optimization) ayuda a que tu contenido aparezca en los primeros resultados de búsqueda. Usa palabras clave relevantes y optimiza títulos.', 'orden': 3, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Ejercicio: Creando un Artículo', 'contenido': 'Crea un artículo corto sobre un tema de tu interés, aplicando los principios aprendidos.', 'orden': 4, 'tipo_contenido': 'ejercicio'},
                ]
            },
            {
                'titulo': 'Seguridad Informática',
                'descripcion': 'Protege tu información y dispositivos contra amenazas digitales como virus, phishing y pérdida de datos.',
                'orden': 4,
                'duracion_estimada': 40,
                'lecciones': [
                    {'titulo': 'Amenazas Comunes', 'contenido': 'Las amenazas más comunes incluyen malware, phishing, ataques de fuerza bruta y pérdida de datos. La prevención es clave.', 'orden': 1, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Contraseñas Seguras', 'contenido': 'Una contraseña segura debe tener al menos 12 caracteres, combinar letras mayúsculas, minúsculas, números y símbolos.', 'orden': 2, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Autenticación Multifactor', 'contenido': 'La autenticación multifactor (MFA) añade una capa extra de seguridad al requerir más de una forma de verificación.', 'orden': 3, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Ejercicio: Evaluando Seguridad', 'contenido': 'Evalúa la seguridad de diferentes contraseñas y sugiere mejoras.', 'orden': 4, 'tipo_contenido': 'ejercicio'},
                ]
            },
            {
                'titulo': 'Resolución de Problemas Técnicos',
                'descripcion': 'Desarrolla habilidades para diagnosticar y resolver problemas técnicos de manera sistemática.',
                'orden': 5,
                'duracion_estimada': 35,
                'lecciones': [
                    {'titulo': 'Enfoque Sistemático', 'contenido': 'Para resolver problemas técnicos, identifica el problema, recopila información, prueba soluciones y documenta el proceso.', 'orden': 1, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Herramientas de Diagnóstico', 'contenido': 'Usa herramientas como el administrador de tareas, logs del sistema y comandos de terminal para diagnosticar problemas.', 'orden': 2, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Prevención de Problemas', 'contenido': 'Mantén tu sistema actualizado, realiza copias de seguridad regulares y usa software confiable.', 'orden': 3, 'tipo_contenido': 'teoria'},
                    {'titulo': 'Ejercicio: Solucionando un Error', 'contenido': 'Simula un problema técnico común y aplica el proceso de resolución paso a paso.', 'orden': 4, 'tipo_contenido': 'ejercicio'},
                ]
            }
        ]

        for modulo_data in modulos_data:
            modulo, created = ModuloEstudio.objects.get_or_create(
                orden=modulo_data['orden'],
                defaults={
                    'titulo': modulo_data['titulo'],
                    'descripcion': modulo_data['descripcion'],
                    'duracion_estimada': modulo_data['duracion_estimada'],
                    'activo': True
                }
            )
            if created:
                for leccion_data in modulo_data['lecciones']:
                    Leccion.objects.create(
                        modulo=modulo,
                        titulo=leccion_data['titulo'],
                        contenido=leccion_data['contenido'],
                        orden=leccion_data['orden'],
                        tipo_contenido=leccion_data['tipo_contenido']
                    )
