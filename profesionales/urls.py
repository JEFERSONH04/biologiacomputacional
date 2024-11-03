from django.urls import path
from profesionales import views
from profesionales.views import busquedaInformacion, agregar_profesional, editar_profesional_view, eliminar_profesional_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', busquedaInformacion.as_view(), name='buscarProfesional'),
    path('agregar_profesional/', agregar_profesional, name='agregar_profesional'),
    path('info_profesional/', views.info_profesional, name='info_profesional'),
    path('id=<int:pk>/', views.detalle_profesional, name='detalle_profesional'),
    path('id=<int:pk>/editar/', editar_profesional_view.as_view(), name='editar'),
    path('id=<int:pk>/eliminar/', eliminar_profesional_view.as_view(), name='eliminar'),
] 