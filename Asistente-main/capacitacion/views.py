from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Modulo, ProgresoUsuario, ResultadoDiagnostico

@login_required
def dashboard(request):
    progresos = ProgresoUsuario.objects.filter(usuario=request.user)
    return render(request, 'capacitacion/dashboard.html', {'progresos': progresos})

@login_required
def diagnostico_modulo(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)
    preguntas = modulo.preguntadiagnostico_set.all()
    
    if request.method == 'POST':
        # Calcular puntaje y determinar si necesita refuerzo
        puntaje = 0
        for pregunta in preguntas:
            respuesta_usuario = request.POST.get(f'pregunta_{pregunta.id}')
            if respuesta_usuario == pregunta.respuesta_correcta:
                puntaje += 1
        
        necesita_refuerzo = puntaje < 3  # Si responde menos de 3 bien
        
        # Guardar resultado
        resultado, created = ResultadoDiagnostico.objects.update_or_create(
            usuario=request.user,
            modulo=modulo,
            defaults={'puntaje': puntaje, 'necesita_refuerzo': necesita_refuerzo}
        )
        
        # Actualizar progreso
        if necesita_refuerzo:
            estado = 'pendiente'
        else:
            estado = 'completado'
            
        ProgresoUsuario.objects.update_or_create(
            usuario=request.user,
            modulo=modulo,
            defaults={'estado': estado}
        )
        
        return redirect('dashboard')
    
    return render(request, 'capacitacion/diagnostico.html', {
        'modulo': modulo,
        'preguntas': preguntas
    })