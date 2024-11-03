from django.contrib import admin
from profesionales.models import InformacionProfesional, Articulos

# Register your models here.

class ProfesionalesFiltro(admin.ModelAdmin):
    search_fields = ("nombre", "apellido", "email", "telefono")

class TablaFiltro(admin.ModelAdmin): # Agregar una tabla con filtros
    list_filter = ("nombre",)

admin.site.register(InformacionProfesional, ProfesionalesFiltro)
admin.site.register(Articulos)