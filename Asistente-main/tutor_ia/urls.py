from django.urls import path
from . import views

app_name = 'tutor_ia'

urlpatterns = [
    path('', views.TutorIAView.as_view(), name='chat'),
    path('enviar-mensaje/', views.TutorIAView.as_view(), name='enviar_mensaje'),
]