from django.contrib import admin
from investigacion.models import CategoriaI, Investigacion, Carrusel

# Register your models here.

admin.site.register(Carrusel)
admin.site.register(CategoriaI)
admin.site.register(Investigacion)