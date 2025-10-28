from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Modulo, Pregunta, DiagnosticoUsuario, RespuestaUsuario, OpcionRespuesta
from .forms import DiagnosticoForm
from modulos.models import ModuloEstudio, ProgresoUsuario
import json

@login_required
@transaction.atomic
def iniciar_diagnostico(request):
    """
    Vista para iniciar el diagnóstico del usuario.
    """
    try:
        diagnostico = DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=False
        ).first()
        
        if not diagnostico:
            diagnostico = DiagnosticoUsuario.objects.create(
                usuario=request.user,
                completado=False,
                fecha_inicio=timezone.now()
            )
        
        preguntas_fijas = [
            {
                'id': 1,
                'texto': '¿Con qué frecuencia usas herramientas ofimáticas (Word, Excel, etc.)?',
                'opciones': [
                    {'id': 1, 'texto': 'Nunca', 'valor': 1},
                    {'id': 2, 'texto': 'Rara vez', 'valor': 2},
                    {'id': 3, 'texto': 'A veces', 'valor': 3},
                    {'id': 4, 'texto': 'Frecuentemente', 'valor': 4},
                    {'id': 5, 'texto': 'Siempre', 'valor': 5}
                ]
            },
            {
                'id': 2,
                'texto': '¿Te sientes cómodo navegando y buscando información en Internet?',
                'opciones': [
                    {'id': 6, 'texto': 'Nunca', 'valor': 1},
                    {'id': 7, 'texto': 'Rara vez', 'valor': 2},
                    {'id': 8, 'texto': 'A veces', 'valor': 3},
                    {'id': 9, 'texto': 'Frecuentemente', 'valor': 4},
                    {'id': 10, 'texto': 'Siempre', 'valor': 5}
                ]
            },
            {
                'id': 3,
                'texto': '¿Has utilizado plataformas de aprendizaje en línea?',
                'opciones': [
                    {'id': 11, 'texto': 'Nunca', 'valor': 1},
                    {'id': 12, 'texto': 'Rara vez', 'valor': 2},
                    {'id': 13, 'texto': 'A veces', 'valor': 3},
                    {'id': 14, 'texto': 'Frecuentemente', 'valor': 4},
                    {'id': 15, 'texto': 'Siempre', 'valor': 5}
                ]
            },
            {
                'id': 4,
                'texto': '¿Sabes cómo proteger tus datos personales en la web?',
                'opciones': [
                    {'id': 16, 'texto': 'Nunca', 'valor': 1},
                    {'id': 17, 'texto': 'Rara vez', 'valor': 2},
                    {'id': 18, 'texto': 'A veces', 'valor': 3},
                    {'id': 19, 'texto': 'Frecuentemente', 'valor': 4},
                    {'id': 20, 'texto': 'Siempre', 'valor': 5}
                ]
            },
            {
                'id': 5,
                'texto': '¿Puedes identificar noticias falsas o desinformación en redes sociales?',
                'opciones': [
                    {'id': 21, 'texto': 'Nunca', 'valor': 1},
                    {'id': 22, 'texto': 'Rara vez', 'valor': 2},
                    {'id': 23, 'texto': 'A veces', 'valor': 3},
                    {'id': 24, 'texto': 'Frecuentemente', 'valor': 4},
                    {'id': 25, 'texto': 'Siempre', 'valor': 5}
                ]
            }
        ]

        if request.method == 'POST':
            # Calcular puntuación total y guardar respuestas
            puntuacion_total = 0
            respuestas_guardadas = []
            for pregunta in preguntas_fijas:
                respuesta_id = request.POST.get(f'pregunta_{pregunta["id"]}')
                if respuesta_id:
                    for opcion in pregunta['opciones']:
                        if str(opcion['id']) == respuesta_id:
                            puntuacion_total += opcion['valor']
                            opcion_obj = OpcionRespuesta.objects.get_or_create(
                                id=opcion['id'],
                                defaults={
                                    'texto': opcion['texto'],
                                    'valor': opcion['valor'],
                                    'pregunta_id': pregunta['id']  
                                }
                            )[0]
                            respuestas_guardadas.append(opcion_obj)
                            break

            # Guardar respuestas en la base de datos
            for i, opcion in enumerate(respuestas_guardadas):
                RespuestaUsuario.objects.create(
                    diagnostico=diagnostico,
                    pregunta_id=preguntas_fijas[i]['id'],
                    opcion_seleccionada=opcion
                )

            # Marcar diagnóstico como completado
            diagnostico.completado = True
            diagnostico.fecha_finalizacion = timezone.now()
            diagnostico.save()

            # Calcular porcentaje (máximo 25 puntos = 5 preguntas × 5 puntos)
            porcentaje = (puntuacion_total / 25) * 100

            messages.success(request, "¡Diagnóstico completado exitosamente!")
            return redirect('diagnostico:resultado_diagnostico')
        
        return render(request, 'diagnostico/cuestionario.html', {
            'preguntas': preguntas_fijas
        })
    
    except Exception as e:
        messages.error(request, f"Error al iniciar el diagnóstico: {str(e)}")
        return redirect('/')

@login_required
def resultado_diagnostico(request):
    """
    Vista para mostrar los resultados del diagnóstico completado
    """
    try:
        # Obtener el último diagnóstico completado del usuario
        diagnostico = DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=True
        ).order_by('-fecha_finalizacion').first()

        if not diagnostico:
            messages.warning(request, "No has completado ningún diagnóstico aún.")
            return redirect('diagnostico:iniciar_diagnostico')

        # Calcular puntuación total desde las respuestas guardadas
        respuestas = RespuestaUsuario.objects.filter(diagnostico=diagnostico).select_related('opcion_seleccionada')
        puntuacion_total = sum(respuesta.opcion_seleccionada.valor for respuesta in respuestas)
        puntuacion_maxima = 25  # 5 preguntas, máximo 5 puntos cada una
        porcentaje = (puntuacion_total / puntuacion_maxima) * 100

        # Generar recomendaciones basadas en la puntuación usando módulos existentes
        from modulos.models import ModuloEstudio
        modulos = ModuloEstudio.objects.filter(activo=True).order_by('orden')

        recomendaciones = []
        if modulos.exists():
            if porcentaje < 40:
                # Recomendar primeros módulos disponibles
                recomendaciones = [modulo.titulo for modulo in modulos[:3]]
            elif porcentaje < 70:
                # Recomendar módulos intermedios
                mid_start = max(0, len(modulos)//2 - 1)
                recomendaciones = [modulo.titulo for modulo in modulos[mid_start:mid_start+3]]
            else:
                # Recomendar módulos avanzados
                recomendaciones = [modulo.titulo for modulo in modulos[len(modulos)//2:]]
        else:
            recomendaciones = ["No hay módulos disponibles actualmente"]

        return render(request, 'diagnostico/resultado.html', {
            'resultados': respuestas,
            'diagnostico': diagnostico,
            'total_preguntas': 5,
            'puntuacion_total_general': puntuacion_total,
            'puntuacion_maxima_general': puntuacion_maxima,
            'porcentaje_general': porcentaje,
            'modulos_evaluados': 1,
            'recomendaciones': recomendaciones,
            'mensaje_generico': 'Gracias por completar el diagnóstico. Basado en tus respuestas, te recomendamos los siguientes módulos:'
        })

    except Exception as e:
        messages.error(request, f"Error al cargar los resultados: {str(e)}")
        return redirect('/')

@login_required
def dashboard_diagnostico(request):
    """
    Dashboard principal del diagnóstico que muestra el progreso del usuario
    """
    try:
        # Obtener diagnóstico activo (no completado)
        diagnostico_activo = DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=False
        ).first()
        
        # Obtener últimos diagnósticos completados
        diagnosticos_completados = DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=True
        ).order_by('-fecha_finalizacion')[:5]  # Últimos 5 diagnósticos
        
        # Obtener estadísticas generales
        total_diagnosticos = DiagnosticoUsuario.objects.filter(usuario=request.user).count()
        diagnosticos_completados_count = DiagnosticoUsuario.objects.filter(
            usuario=request.user, 
            completado=True
        ).count()
        
        return render(request, 'diagnostico/dashboard_diagnostico.html', {
            'diagnostico_activo': diagnostico_activo,
            'diagnosticos_completados': diagnosticos_completados,
            'total_diagnosticos': total_diagnosticos,
            'diagnosticos_completados_count': diagnosticos_completados_count,
            'porcentaje_completados': (diagnosticos_completados_count / total_diagnosticos * 100) if total_diagnosticos > 0 else 0
        })

    except Exception as e:
        messages.error(request, f"Error al cargar el dashboard: {str(e)}")
        return render(request, 'diagnostico/dashboard_diagnostico.html', {
            'diagnostico_activo': None,
            'diagnosticos_completados': [],
            'error': str(e)
        })

@login_required
def reiniciar_diagnostico(request):
    """
    Vista para reiniciar el diagnóstico actual
    """
    try:
        # Eliminar diagnóstico actual no completado
        DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=False
        ).delete()

        messages.info(request, "Diagnóstico reiniciado. Puedes comenzar de nuevo.")
        return redirect('diagnostico:iniciar_diagnostico')

    except Exception as e:
        messages.error(request, f"Error al reiniciar el diagnóstico: {str(e)}")
        return redirect('/')

@login_required
def dashboard_progreso(request):
    """
    Vista para mostrar el progreso del usuario en los módulos de estudio
    """
    try:
        # Obtener todos los módulos activos
        total_modulos = ModuloEstudio.objects.filter(activo=True).count()

        # Obtener progreso del usuario
        progresos = ProgresoUsuario.objects.filter(usuario=request.user)

        # Calcular módulos completados
        modulos_completados = progresos.filter(completado=True).count()

        # Calcular porcentaje de progreso
        porcentaje_progreso = (modulos_completados / total_modulos * 100) if total_modulos > 0 else 0

        # Construir datos para la tabla
        datos_modulos = []
        for modulo in ModuloEstudio.objects.filter(activo=True).order_by('orden'):
            progreso = progresos.filter(modulo=modulo).first()
            if progreso and progreso.completado:
                estado = 'Completado'
            elif progreso:
                estado = 'En progreso'
            else:
                estado = 'No iniciado'
            datos_modulos.append({
                'modulo': modulo,
                'estado': estado
            })

        return render(request, 'diagnostico/dashboard_progreso.html', {
            'modulos_completados': modulos_completados,
            'total_modulos': total_modulos,
            'porcentaje_progreso': round(porcentaje_progreso),
            'datos_modulos': datos_modulos,
            'progresos': progresos
        })

    except Exception as e:
        messages.error(request, f"Error al cargar el progreso: {str(e)}")
        return render(request, 'diagnostico/dashboard_progreso.html', {
            'modulos_completados': 0,
            'total_modulos': 0,
            'porcentaje_progreso': 0,
            'datos_modulos': [],
            'progresos': [],
            'error': str(e)
        })
