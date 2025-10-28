from django import forms
from .models import Pregunta, OpcionRespuesta

class DiagnosticoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        preguntas = kwargs.pop('preguntas')
        super(DiagnosticoForm, self).__init__(*args, **kwargs)
        
        for pregunta in preguntas:
            opciones = [(op.id, op.texto) for op in pregunta.opcionrespuesta_set.all()]
            self.fields[f'pregunta_{pregunta.id}'] = forms.ChoiceField(
                choices=opciones,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                label=pregunta.texto,
                required=True
            )
    
    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if field_name.startswith('pregunta_') and not value:
                pregunta_id = field_name.replace('pregunta_', '')
                self.add_error(field_name, 'Esta pregunta es requerida')
        return cleaned_data