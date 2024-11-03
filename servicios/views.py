from django.views.generic import TemplateView
from servicios.models import Categoria, Servicio
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import request
from BiologiaComputacional.forms import ServicioForm
import os
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

# Definir permisos


def is_superuser(user):

    return user.is_superuser


def is_staff(user):

    return user.is_staff


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

# Vista para mostrar todas las herramientas


class herramientas_view(TemplateView):
    template_name = "servicios/herramientas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        herramientas = Servicio.objects.filter(
            categoria__nombre_categoria='Herramienta')
        form_submitted = False

        if query:
            herramientas = herramientas.filter(
                Q(nombre__icontains=query)
            )
            cantidad_herramientas_buscadas = herramientas.count()
            form_submitted = True
        else:
            cantidad_herramientas_buscadas = herramientas.count()

        cantidad_total_db = Servicio.objects.filter(
            categoria__nombre_categoria='Base de Datos').count()
        cantidad_total_herramientas = Servicio.objects.filter(
            categoria__nombre_categoria='Herramienta').count()

        context['cantidad_db'] = cantidad_total_db
        context['herramientas'] = herramientas
        context['cantidad_herramientas'] = cantidad_total_herramientas
        context['cantidad_herramientas_buscadas'] = cantidad_herramientas_buscadas
        context['form_submitted'] = form_submitted
        return context


# Vista para mostrar todas las bases de datos
class bases_de_datos_view(TemplateView):
    template_name = "servicios/bases_de_datos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        db = Servicio.objects.filter(
            categoria__nombre_categoria='Base de Datos')
        form_submitted = False

        if query:
            db = db.filter(
                Q(nombre__icontains=query)
            )
            cantidad_db_buscadas = db.count()
            form_submitted = True
        else:
            cantidad_db_buscadas = db.count()

        cantidad_total_herramientas = Servicio.objects.filter(
            categoria__nombre_categoria='Herramienta').count()
        cantidad_total_db = Servicio.objects.filter(
            categoria__nombre_categoria='Base de Datos').count()

        context['db'] = db
        context['cantidad_db'] = cantidad_total_db
        context['cantidad_herramientas'] = cantidad_total_herramientas
        context['cantidad_db_buscadas'] = cantidad_db_buscadas
        context['form_submitted'] = form_submitted
        return context


# Vista para mostrar la informacion de las herramientas o bases de datos

@method_decorator(login_required, name='dispatch')
class servicios_detalle_view(TemplateView):
    template_name = "servicios/servicios_detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio_nombre = kwargs.get('nombre')

        servicio = get_object_or_404(Servicio, nombre=servicio_nombre)

        servicios_herramienta = Servicio.objects.filter(
            categoria__nombre_categoria='Herramienta').exclude(nombre=servicio_nombre)

        servicios_db = Servicio.objects.filter(
            categoria__nombre_categoria='Base de Datos').exclude(nombre=servicio_nombre)

        context['servicios_herramienta'] = servicios_herramienta
        context['servicios_db'] = servicios_db
        context['servicio'] = servicio
        return context
    
    def post(self, request, nombre):
        servicio = get_object_or_404(Servicio, nombre=nombre)
        
        servicio.delete()
        
        messages.success(request, 'Servicio eliminado correctamente')
        
        return redirect('servicios')

# Vista para editar la informacion de las herramientas o bases de datos

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser), name='dispatch')
class servicio_edit_view(TemplateView):
    template_name = "servicios/servicio_edit.html"
    
    def get(self, request, nombre):
        servicio = get_object_or_404(Servicio, nombre=nombre)
        form = ServicioForm(instance=servicio)
        categorias = Categoria.objects.all()

        context = {
            'servicio': servicio,
            'form': form,
            'categorias': categorias
        }

        return render(request, self.template_name, context)
    
    def post(self, request, nombre):
        servicio = get_object_or_404(Servicio, nombre=nombre)
        form = ServicioForm(request.POST, request.FILES, instance=servicio)
        categorias = Categoria.objects.all()

        if 'delete_file' in request.POST:
            servicio.archivo.delete()
            servicio.archivo = None
            servicio.save()

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Información actualizada correctamente')
            return redirect('servicios_detalle', servicio.nombre)
        else:
            context = {
                'servicio': servicio,
                'form': form,
                'categorias': categorias,
                'form_errors': form.errors
            }
            return render(request, self.template_name, context)
        
        
# Vista para agregar una herramienta o base de datos


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser), name='dispatch')
class nuevo_servicio_view(TemplateView):
    template_name = "servicios/nuevo_servicio.html"

    def get(self, request):
        form = ServicioForm()
        categorias = Categoria.objects.all()
        
        context = {
            'form': form,
            'categorias': categorias
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = ServicioForm(request.POST, request.FILES)
        categorias = Categoria.objects.all()
        
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.save()
            messages.success(request, 'Servicio agregado correctamente')
            
            return redirect('servicios_detalle', servicio.nombre)
        
        else:
            context = {
                'form': form,
                'form_errors': form.errors,
                'categorias': categorias
            }
            
            return render(request, self.template_name, context)
        