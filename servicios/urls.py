from django.urls import path
from servicios import views

urlpatterns = [
    path('', views.herramientas_view.as_view(), name='servicios'),
    path('bases-de-datos/', views.bases_de_datos_view.as_view(), name='database'),
    path('nuevo-servicio/', views.nuevo_servicio_view.as_view(), name='nuevo_servicio'),
    path('<str:nombre>/', views.servicios_detalle_view.as_view(), name='servicios_detalle'),
    path('<str:nombre>/editar/', views.servicio_edit_view.as_view(), name='servicios_editar'),
] 