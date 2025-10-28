from django.urls import path
from . import views

app_name = 'modulos'

urlpatterns = [
    path('', views.lista_modulos, name='lista_modulos'),

    path('<int:modulo_id>/', views.detalle_modulo, name='detalle_modulo'),
    path('<int:modulo_id>/certificado/', views.descargar_certificado, name='descargar_certificado'),
]
