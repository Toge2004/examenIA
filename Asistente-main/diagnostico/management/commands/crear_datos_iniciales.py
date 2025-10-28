from django.core.management.base import BaseCommand
from diagnostico.models import Pregunta, Modulo, OpcionRespuesta

class Command(BaseCommand):
    help = 'Crear datos iniciales para el diagnóstico'

    def handle(self, *args, **options):
        # Crear módulo si no existe
        modulo, created = Modulo.objects.get_or_create(
            nombre='Competencias Digitales',
            defaults={'descripcion': 'Diagnóstico de competencias digitales básicas'}
        )
        self.stdout.write(f'Módulo creado: {created}')

        # Crear preguntas fijas
        preguntas_data = [
            {'id': 1, 'texto': '¿Con qué frecuencia usas herramientas ofimáticas (Word, Excel, etc.)?'},
            {'id': 2, 'texto': '¿Te sientes cómodo navegando y buscando información en Internet?'},
            {'id': 3, 'texto': '¿Has utilizado plataformas de aprendizaje en línea?'},
            {'id': 4, 'texto': '¿Sabes cómo proteger tus datos personales en la web?'},
            {'id': 5, 'texto': '¿Puedes identificar noticias falsas o desinformación en redes sociales?'}
        ]

        for p_data in preguntas_data:
            pregunta, created = Pregunta.objects.get_or_create(
                id=p_data['id'],
                defaults={
                    'modulo': modulo,
                    'texto': p_data['texto'],
                    'orden': p_data['id']
                }
            )
            self.stdout.write(f'Pregunta {p_data["id"]} creada: {created}')

        # Crear opciones para cada pregunta
        opciones_data = [
            {'id': 1, 'pregunta_id': 1, 'texto': 'Nunca', 'valor': 1},
            {'id': 2, 'pregunta_id': 1, 'texto': 'Rara vez', 'valor': 2},
            {'id': 3, 'pregunta_id': 1, 'texto': 'A veces', 'valor': 3},
            {'id': 4, 'pregunta_id': 1, 'texto': 'Frecuentemente', 'valor': 4},
            {'id': 5, 'pregunta_id': 1, 'texto': 'Siempre', 'valor': 5},
            {'id': 6, 'pregunta_id': 2, 'texto': 'Nunca', 'valor': 1},
            {'id': 7, 'pregunta_id': 2, 'texto': 'Rara vez', 'valor': 2},
            {'id': 8, 'pregunta_id': 2, 'texto': 'A veces', 'valor': 3},
            {'id': 9, 'pregunta_id': 2, 'texto': 'Frecuentemente', 'valor': 4},
            {'id': 10, 'pregunta_id': 2, 'texto': 'Siempre', 'valor': 5},
            {'id': 11, 'pregunta_id': 3, 'texto': 'Nunca', 'valor': 1},
            {'id': 12, 'pregunta_id': 3, 'texto': 'Rara vez', 'valor': 2},
            {'id': 13, 'pregunta_id': 3, 'texto': 'A veces', 'valor': 3},
            {'id': 14, 'pregunta_id': 3, 'texto': 'Frecuentemente', 'valor': 4},
            {'id': 15, 'pregunta_id': 3, 'texto': 'Siempre', 'valor': 5},
            {'id': 16, 'pregunta_id': 4, 'texto': 'Nunca', 'valor': 1},
            {'id': 17, 'pregunta_id': 4, 'texto': 'Rara vez', 'valor': 2},
            {'id': 18, 'pregunta_id': 4, 'texto': 'A veces', 'valor': 3},
            {'id': 19, 'pregunta_id': 4, 'texto': 'Frecuentemente', 'valor': 4},
            {'id': 20, 'pregunta_id': 4, 'texto': 'Siempre', 'valor': 5},
            {'id': 21, 'pregunta_id': 5, 'texto': 'Nunca', 'valor': 1},
            {'id': 22, 'pregunta_id': 5, 'texto': 'Rara vez', 'valor': 2},
            {'id': 23, 'pregunta_id': 5, 'texto': 'A veces', 'valor': 3},
            {'id': 24, 'pregunta_id': 5, 'texto': 'Frecuentemente', 'valor': 4},
            {'id': 25, 'pregunta_id': 5, 'texto': 'Siempre', 'valor': 5}
        ]

        for o_data in opciones_data:
            opcion, created = OpcionRespuesta.objects.get_or_create(
                id=o_data['id'],
                defaults={
                    'pregunta_id': o_data['pregunta_id'],
                    'texto': o_data['texto'],
                    'valor': o_data['valor']
                }
            )
            self.stdout.write(f'Opción {o_data["id"]} creada: {created}')

        self.stdout.write('Datos iniciales creados exitosamente.')
