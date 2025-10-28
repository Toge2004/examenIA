from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer
from io import BytesIO
from .models import ModuloEstudio, ProgresoUsuario


@login_required
def lista_modulos(request):
    # Obtener módulos reales de la base de datos
    modulos = ModuloEstudio.objects.filter(activo=True).order_by('orden')

    # Obtener recomendaciones del diagnóstico si existe
    recomendaciones = []
    try:
        from diagnostico.models import DiagnosticoUsuario, RespuestaUsuario
        diagnostico = DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=True
        ).order_by('-fecha_finalizacion').first()

        if diagnostico:
            respuestas = RespuestaUsuario.objects.filter(diagnostico=diagnostico).select_related('opcion_seleccionada')
            puntuacion_total = sum(respuesta.opcion_seleccionada.valor for respuesta in respuestas)
            porcentaje = (puntuacion_total / 25) * 100

            # Generar recomendaciones basadas en la puntuación
            if porcentaje < 40:
                # Recomendar primeros módulos
                recomendaciones = [modulo.titulo for modulo in modulos[:3]]
            elif porcentaje < 70:
                # Recomendar módulos intermedios
                mid_start = max(0, len(modulos)//2 - 1)
                recomendaciones = [modulo.titulo for modulo in modulos[mid_start:mid_start+3]]
            else:
                # Recomendar módulos avanzados
                recomendaciones = [modulo.titulo for modulo in modulos[len(modulos)//2:]]
    except:
        pass  # Si no hay diagnóstico, mostrar todos los módulos

    # Filtrar módulos si hay recomendaciones
    if recomendaciones:
        modulos_filtrados = modulos.filter(titulo__in=recomendaciones)
    else:
        modulos_filtrados = modulos

    return render(request, 'modulos/lista_modulos.html', {
        'modulos': modulos_filtrados,
        'recomendaciones': recomendaciones,
        'todos_modulos': modulos if recomendaciones else None
    })


@login_required
def detalle_modulo(request, modulo_id):
    try:
        modulo = ModuloEstudio.objects.get(id=modulo_id, activo=True)
    except ModuloEstudio.DoesNotExist:
        raise Http404("Módulo no encontrado")

    titulo = modulo.titulo
    orden = modulo.orden

    # Preguntas específicas por módulo (10 por módulo)
    QUESTIONS = {
        1: [
            {
                'texto': '¿Qué es el sistema binario y por qué es importante en la informática?',
                'opciones': {'A': 'Un sistema de base 2 usado para representar datos en computadoras', 'B': 'Un lenguaje de programación', 'C': 'Un tipo de hardware', 'D': 'Un protocolo de red'},
                'correcta': 'A'
            },
            {
                'texto': '¿Cuál es la función principal de un sistema operativo?',
                'opciones': {'A': 'Crear contenido multimedia', 'B': 'Gestionar recursos y permitir la ejecución de programas', 'C': 'Conectar solo impresoras', 'D': 'Proteger contra virus automáticamente'},
                'correcta': 'B'
            },
            {
                'texto': '¿Qué diferencia hay entre hardware y software?',
                'opciones': {'A': 'Hardware es físico; software son programas e instrucciones', 'B': 'No hay diferencia', 'C': 'Hardware es más barato', 'D': 'Software es siempre de código abierto'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué es una red y cuál es su propósito básico?',
                'opciones': {'A': 'Conectar dispositivos para compartir recursos e información', 'B': 'Almacenar datos localmente', 'C': 'Editar imágenes', 'D': 'Crear respaldos automáticos'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué componente se encarga de procesar las instrucciones (CPU)?',
                'opciones': {'A': 'La memoria RAM', 'B': 'El disco duro', 'C': 'La unidad central de procesamiento (CPU)', 'D': 'La tarjeta gráfica'},
                'correcta': 'C'
            },
            {
                'texto': '¿Qué entendemos por datos y cómo se almacenan comúnmente?',
                'opciones': {'A': 'Información que puede ser almacenada en formatos digitales como archivos y bases de datos', 'B': 'Solo texto impreso', 'C': 'Solo imágenes físicas', 'D': 'Datos no se almacenan'},
                'correcta': 'A'
            },
            {
                'texto': '¿Cuál es la función de la memoria RAM en un equipo?',
                'opciones': {'A': 'Almacenar datos permanentemente', 'B': 'Proveer almacenamiento temporal para procesos en ejecución', 'C': 'Controlar la pantalla', 'D': 'Gestionar la red'},
                'correcta': 'B'
            },
            {
                'texto': '¿Qué es una aplicación y cómo se instala en un dispositivo?',
                'opciones': {'A': 'Un programa que cumple funciones específicas y se instala mediante instaladores o tiendas de apps', 'B': 'Un componente de hardware', 'C': 'Un tipo de cable', 'D': 'Un virus'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué papel tiene Internet en la comunicación entre equipos?',
                'opciones': {'A': 'Permitir la interconexión global y el intercambio de información', 'B': 'Almacenar físicamente los equipos', 'C': 'Crear hardware', 'D': 'Sustituir la electricidad'},
                'correcta': 'A'
            },
            {
                'texto': '¿Por qué es importante actualizar el software regularmente?',
                'opciones': {'A': 'Para obtener mejoras, correcciones de errores y parches de seguridad', 'B': 'No es importante', 'C': 'Solo para cambiar colores', 'D': 'Para borrar archivos'},
                'correcta': 'A'
            }
        ],
        2: [
            {
                'texto': '¿Qué buenas prácticas forman parte de la netiqueta en comunicación digital?',
                'opciones': {'A': 'Usar mayúsculas para enfatizar', 'B': 'Ser claro, respetuoso y citar fuentes', 'C': 'Enviar mensajes sin revisar', 'D': 'Ignorar solicitudes de aclaración'},
                'correcta': 'B'
            },
            {
                'texto': '¿Cuál es la ventaja principal del correo electrónico frente a la mensajería instantánea?',
                'opciones': {'A': 'Mayor formalidad y registro histórico de comunicaciones', 'B': 'Respuestas más rápidas siempre', 'C': 'No requiere conexión a Internet', 'D': 'Es gratuito siempre'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué aspectos hay que considerar al compartir información en redes sociales?',
                'opciones': {'A': 'Privacidad, veracidad y relevancia para la audiencia', 'B': 'Compartir todo sin filtrar', 'C': 'Usar sólo imágenes', 'D': 'Ignorar términos de servicio'},
                'correcta': 'A'
            },
            {
                'texto': '¿Cómo mejora la comunicación digital la colaboración en equipos remotos?',
                'opciones': {'A': 'Permite coordinar tareas y compartir documentos en tiempo real', 'B': 'Evita la comunicación por completo', 'C': 'Solo sirve para chatear', 'D': 'Sustituye la necesidad de liderazgo'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué es el tono apropiado al escribir mensajes profesionales?',
                'opciones': {'A': 'Formal, claro y respetuoso', 'B': 'Irónico y sarcástico', 'C': 'Extremadamente informal', 'D': 'Vago y confuso'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué formato es adecuado para compartir un documento editable?',
                'opciones': {'A': 'PDF no editable', 'B': 'Documento en la nube con permisos adecuados (por ejemplo Google Docs)', 'C': 'Imagen del documento', 'D': 'Archivo binario propietario sin permisos'},
                'correcta': 'B'
            },
            {
                'texto': '¿Cómo afecta la accesibilidad a la comunicación digital?',
                'opciones': {'A': 'Permite que más personas, incluidas con discapacidades, accedan al contenido', 'B': 'No tiene impacto', 'C': 'Solo es relevante en televisión', 'D': 'Reduce la audiencia'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué riesgos de privacidad existen al comunicarse en línea?',
                'opciones': {'A': 'Exposición de datos personales y suplantación de identidad', 'B': 'No existen riesgos', 'C': 'Solo afecta a empresas grandes', 'D': 'Solamente pérdida de archivos'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué diferencia hay entre canales síncronos y asíncronos?',
                'opciones': {'A': 'Síncronos son en tiempo real; asíncronos permiten respuesta diferida', 'B': 'No hay diferencia', 'C': 'Asíncronos requieren videollamada', 'D': 'Síncronos siempre son escritos'},
                'correcta': 'A'
            },
            {
                'texto': '¿Por qué es importante verificar la fuente antes de reenviar información?',
                'opciones': {'A': 'Para evitar difundir información falsa o malintencionada', 'B': 'No es importante', 'C': 'Siempre es responsabilidad de otros', 'D': 'Porque ocupa menos espacio'},
                'correcta': 'A'
            }
        ],
        3: [
            {
                'texto': '¿Qué elementos conforman una buena estructura de contenido (introducción, desarrollo, cierre)?',
                'opciones': {'A': 'Introducción clara, desarrollo coherente y cierre que sintetiza', 'B': 'Solo título largo', 'C': 'Solo imágenes', 'D': 'Texto desordenado'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué importancia tiene el título al crear contenido para la web?',
                'opciones': {'A': 'Atrae a la audiencia y mejora el SEO', 'B': 'No tiene importancia', 'C': 'Solo sirve para imprimir', 'D': 'Debe ser muy largo'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué es SEO y por qué influye en la visibilidad del contenido?',
                'opciones': {'A': 'Prácticas para mejorar posicionamiento en buscadores', 'B': 'Un tipo de imagen', 'C': 'Solo anuncios pagados', 'D': 'Un lenguaje de programación'},
                'correcta': 'A'
            },
            {
                'texto': '¿Cómo elegir el formato adecuado (texto, imagen, video) según el mensaje?',
                'opciones': {'A': 'Depende de la audiencia, objetivo y plataforma', 'B': 'Siempre elegir video', 'C': 'Siempre texto', 'D': 'Elegir al azar'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué prácticas ayudan a que el contenido sea accesible para todos?',
                'opciones': {'A': 'Usar texto alternativo en imágenes y subtítulos en videos', 'B': 'Evitar descripciones', 'C': 'Usar solo colores sin contraste', 'D': 'Ignorar accesibilidad'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué herramientas básicas se usan para editar imágenes o video?',
                'opciones': {'A': 'Programas como GIMP, Photoshop o herramientas en línea', 'B': 'Solo procesador de texto', 'C': 'No existen herramientas', 'D': 'Solo hardware caro'},
                'correcta': 'A'
            },
            {
                'texto': '¿Por qué respetar los derechos de autor al usar recursos ajenos?',
                'opciones': {'A': 'Para evitar problemas legales y reconocer el trabajo ajeno', 'B': 'No es necesario', 'C': 'Solo para obras antiguas', 'D': 'Porque es más rápido'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué es un guion y por qué ayuda en la creación multimedia?',
                'opciones': {'A': 'Un plan que organiza contenido y facilita la producción', 'B': 'Un tipo de cámara', 'C': 'Un editor de video', 'D': 'Un formato de imagen'},
                'correcta': 'A'
            },
            {
                'texto': '¿Cómo se adapta el contenido a la audiencia objetivo?',
                'opciones': {'A': 'Ajustando tono, formato y nivel de profundidad', 'B': 'Usando siempre el mismo estilo', 'C': 'Ignorando a la audiencia', 'D': 'Copiando otros contenidos'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué métricas sirven para evaluar el rendimiento de un contenido?',
                'opciones': {'A': 'Visitas, tiempo de permanencia, tasa de conversión y compartidos', 'B': 'Solo la longitud del texto', 'C': 'El número de archivos en el ordenador', 'D': 'Ninguna métrica'},
                'correcta': 'A'
            }
        ],
        4: [
            {
                'texto': '¿Qué características debe tener una contraseña segura?',
                'opciones': {'A': 'Corta y basada en una palabra común', 'B': 'Larga, con letras, números y símbolos', 'C': 'Solo números repetidos', 'D': 'El nombre del usuario'},
                'correcta': 'B'
            },
            {
                'texto': '¿Qué es el phishing y cómo identificarlo?',
                'opciones': {'A': 'Una técnica para intentar engañar solicitando datos; suele presentar enlaces sospechosos y errores', 'B': 'Un antivirus', 'C': 'Un tipo de hardware', 'D': 'Un navegador'},
                'correcta': 'A'
            },
            {
                'texto': '¿Por qué son importantes las actualizaciones de seguridad?',
                'opciones': {'A': 'Corrigen vulnerabilidades y mejoran la protección del sistema', 'B': 'Solo cambian colores', 'C': 'Siempre rompen el sistema', 'D': 'No son necesarias'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué es el cifrado y cuándo se utiliza?',
                'opciones': {'A': 'Transformar datos para que solo personas autorizadas puedan leerlos; se usa en comunicaciones y almacenamiento', 'B': 'Borrar datos', 'C': 'Acelerar la CPU', 'D': 'Un protocolo de video'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué prácticas ayudan a proteger la privacidad en línea?',
                'opciones': {'A': 'Compartir contraseñas con amigos', 'B': 'Configurar privacidad, limitar datos compartidos y usar MFA', 'C': 'Publicar ubicación constantemente', 'D': 'Usar software pirata'},
                'correcta': 'B'
            },
            {
                'texto': '¿Qué es el malware y cómo se puede prevenir su instalación?',
                'opciones': {'A': 'Software malicioso; prevenir con antivirus, no abrir archivos sospechosos y actualizar', 'B': 'Una app segura', 'C': 'Un tipo de hardware', 'D': 'Siempre inofensivo'},
                'correcta': 'A'
            },
            {
                'texto': '¿Cuál es la utilidad de realizar copias de seguridad regularmente?',
                'opciones': {'A': 'Recuperar datos ante fallos, pérdidas o ataques', 'B': 'Ocultar archivos', 'C': 'Acelerar el equipo', 'D': 'Eliminar datos'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué es la autenticación multifactor (MFA) y por qué usarla?',
                'opciones': {'A': 'Un método que combina varias verificaciones para aumentar la seguridad', 'B': 'Usar la misma contraseña en todos lados', 'C': 'Un tipo de firewall', 'D': 'Un sistema operativo'},
                'correcta': 'A'
            },
            {
                'texto': '¿Cómo asegurar una red Wi‑Fi doméstica básica?',
                'opciones': {'A': 'Dejar la configuración por defecto', 'B': 'Cambiar la contraseña, usar cifrado WPA2/3 y ocultar SSID', 'C': 'Usar contraseñas simples', 'D': 'Compartir la contraseña públicamente'},
                'correcta': 'B'
            },
            {
                'texto': '¿Qué precauciones tomar al conectar dispositivos USB desconocidos?',
                'opciones': {'A': 'Conectarlos sin precaución', 'B': 'Evitar conectarlos y analizarlos en un entorno seguro', 'C': 'Usarlos para restaurar sistema', 'D': 'Formatearlos automáticamente'},
                'correcta': 'B'
            }
        ],
        5: [
            {
                'texto': '¿Cuál es el primer paso al enfrentar un problema técnico?',
                'opciones': {'A': 'Ignorar el problema', 'B': 'Reproducir y describir el problema claramente', 'C': 'Reiniciar sin investigar', 'D': 'Desinstalar todo'},
                'correcta': 'B'
            },
            {
                'texto': '¿Qué técnicas ayudan a diagnosticar la causa raíz de un fallo?',
                'opciones': {'A': 'Aislar variables, revisar logs y repetir pasos', 'B': 'Cambiar muchas cosas a la vez', 'C': 'Suponer sin pruebas', 'D': 'Borrar registros'},
                'correcta': 'A'
            },
            {
                'texto': '¿Por qué es útil reproducir el error paso a paso?',
                'opciones': {'A': 'Para entender las condiciones que lo producen y facilitar la solución', 'B': 'No aporta información', 'C': 'Solo para probar hardware', 'D': 'Oculta la causa'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué información debemos recopilar antes de pedir ayuda?',
                'opciones': {'A': 'Detalles del error, pasos para reproducirlo y logs relevantes', 'B': 'Solo la hora actual', 'C': 'Datos irrelevantes', 'D': 'Nada'},
                'correcta': 'A'
            },
            {
                'texto': '¿Cómo priorizar problemas cuando hay varios pendientes?',
                'opciones': {'A': 'Por impacto y urgencia', 'B': 'Por orden aleatorio', 'C': 'Por preferencia personal', 'D': 'Por tamaño del archivo'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué papel juegan las pruebas al validar una solución?',
                'opciones': {'A': 'Verifican que la solución funciona y no introduce nuevos errores', 'B': 'No son necesarias', 'C': 'Solo retrasan el trabajo', 'D': 'Sustituyen la documentación'},
                'correcta': 'A'
            },
            {
                'texto': '¿Cómo documentar una solución para que otros la reutilicen?',
                'opciones': {'A': 'Describir pasos, causas y comandos usados claramente', 'B': 'Usar lenguaje críptico', 'C': 'No documentar', 'D': 'Solo guardar imágenes'},
                'correcta': 'A'
            },
            {
                'texto': '¿Por qué es importante aislar variables al depurar un error?',
                'opciones': {'A': 'Para identificar la fuente exacta del problema', 'B': 'Porque es más rápido sin pruebas', 'C': 'Para ocultar el problema', 'D': 'No tiene sentido'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué herramientas comunes ayudan a resolver problemas (logs, debugger)?',
                'opciones': {'A': 'Logs, depuradores, monitorización y pruebas unitarias', 'B': 'Solo una linterna', 'C': 'Herramientas físicas únicamente', 'D': 'Ninguna'},
                'correcta': 'A'
            },
            {
                'texto': '¿Qué acciones tomar si una solución temporal funciona pero no es definitiva?',
                'opciones': {'A': 'Documentar la solución temporal y planear una reparación definitiva', 'B': 'Olvidar el problema', 'C': 'No comunicar a nadie', 'D': 'Eliminar registros'},
                'correcta': 'A'
            }
        ],
    }

    entradas = QUESTIONS.get(orden)
    if not entradas:
        raise Http404("No se encontraron preguntas para este módulo")

    # Manejar envío de respuestas via POST
    resultado = None
    feedback = []
    respuestas_usuario = {}
    if request.method == 'POST':
        for i in range(1, len(entradas) + 1):
            key = f'pregunta_{i}'
            respuestas_usuario[i] = request.POST.get(key)

        puntaje = 0
        for i, entrada in enumerate(entradas, start=1):
            correcta = entrada['correcta']
            dada = respuestas_usuario.get(i)
            es_correcta = (dada == correcta)
            if es_correcta:
                puntaje += 1
            feedback.append({
                'numero': i,
                'correcta': correcta,
                'dada': dada,
                'es_correcta': es_correcta,
                'texto': entrada['texto']
            })

        resultado = {
            'puntaje': puntaje,
            'total': len(entradas)
        }

        # Marcar como completado si aprueba (70% o más)
        if puntaje >= 7:
            progreso, created = ProgresoUsuario.objects.get_or_create(
                usuario=request.user,
                modulo=modulo,
                defaults={'completado': True, 'fecha_completado': timezone.now(), 'puntuacion': puntaje}
            )
            if not created and not progreso.completado:
                progreso.completado = True
                progreso.fecha_completado = timezone.now()
                progreso.puntuacion = puntaje
                progreso.save()

    preguntas = []
    for i, entrada in enumerate(entradas, start=1):
        preguntas.append({
            'numero': i,
            'texto': entrada['texto'],
            'opciones': entrada['opciones'],
            'correcta': entrada['correcta'],
            'seleccion': respuestas_usuario.get(i)
        })

    lecciones = modulo.lecciones.all()

    # Verificar si el módulo está completado
    completado = False
    try:
        progreso = ProgresoUsuario.objects.get(usuario=request.user, modulo=modulo)
        completado = progreso.completado
    except ProgresoUsuario.DoesNotExist:
        pass

    context = {
        'modulo': modulo,
        'titulo': titulo,
        'lecciones': lecciones,
        'preguntas': preguntas,
        'resultado': resultado,
        'feedback': feedback,
        'completado': completado,
    }

    return render(request, 'modulos/detalle_modulo.html', context)


@login_required
def descargar_certificado(request, modulo_id):
    modulo = get_object_or_404(ModuloEstudio, id=modulo_id, activo=True)
    progreso = get_object_or_404(ProgresoUsuario, usuario=request.user, modulo=modulo, completado=True)

    # Crear PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Título
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - 100, "CERTIFICADO DE COMPLETACIÓN")

    # Nombre del usuario
    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2, height - 150, f"Otorgado a: {request.user.get_full_name() or request.user.username}")

    # Módulo completado
    p.setFont("Helvetica", 16)
    p.drawCentredString(width / 2, height - 200, f"Por completar el módulo: {modulo.titulo}")

    # Fecha y puntuación
    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2, height - 250, f"Fecha de completación: {progreso.fecha_completado.strftime('%d/%m/%Y')}")
    p.drawCentredString(width / 2, height - 280, f"Puntuación obtenida: {progreso.puntuacion}/10")

    # Firma
    p.setFont("Helvetica-Oblique", 12)
    p.drawCentredString(width / 2, height - 350, "Plataforma Adaptativa de Aprendizaje")

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{modulo.titulo.replace(" ", "_")}.pdf"'
    return response
