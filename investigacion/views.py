from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from investigacion.models import CategoriaI, Investigacion, Carrusel
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from BiologiaComputacional.forms import InvestigacionForm, CarruselForm
from django.contrib import messages
from django.urls import reverse_lazy


# Create your views here.


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

# Vista para ver informacion de las investigaciones


class investigacion_view(TemplateView):
    template_name = "investigacion/investigacion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaI.objects.all()
        context['carrusel'] = Carrusel.objects.first()
        return context


# Vista para editar texto y carrusel de fotos

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser), name='dispatch')
class InvestigacionCarruselEditView(TemplateView):
    template_name = "investigacion/investigacion_edit_carrusel.html"

    def get(self, request, *args, **kwargs):
        carrusel = Carrusel.objects.first()
        form = CarruselForm(instance=carrusel)

        context = {
            'carrusel': carrusel,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        carrusel = Carrusel.objects.first()
        form = CarruselForm(request.POST, request.FILES, instance=carrusel)

        if form.is_valid():
            form.save()
            messages.success(request, 'Carrusel actualizado correctamente.')
            return redirect('investigacion')
        else:
            context = {
                'carrusel': carrusel,
                'form': form,
                'form_errors': form.errors
            }
            return render(request, self.template_name, context)


# Vista para editar informacion de las investigaciones


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser), name='dispatch')
class InvestigacionEditView(TemplateView):
    template_name = "investigacion/investigacion_edit.html"

    def get(self, request, nombre):
        investigacion = get_object_or_404(Investigacion, nombre=nombre)
        form = InvestigacionForm(instance=investigacion)
        categorias = CategoriaI.objects.all()

        context = {
            'investigacion': investigacion,
            'form': form,
            'categorias': categorias
        }

        return render(request, self.template_name, context)

    def post(self, request, nombre):
        investigacion = get_object_or_404(Investigacion, nombre=nombre)
        form = InvestigacionForm(
            request.POST, request.FILES, instance=investigacion)
        categorias = CategoriaI.objects.all()

        if 'delete_file_imagen_tif' in request.POST:
            investigacion.imagen_tif.delete()
            investigacion.imagen_tif = None
            investigacion.save()

        if 'delete_file_pdf' in request.POST:
            investigacion.pdf.delete()
            investigacion.pdf = None
            investigacion.save()

        if 'delete_file_mejores' in request.POST:
            investigacion.mejores_pdf.delete()
            investigacion.mejores_pdf = None
            investigacion.save()

        if 'delete_file_imagen_extra1' in request.POST:
            investigacion.imagen_extra_1.delete()
            investigacion.imagen_extra_1 = None
            investigacion.save()

        if 'delete_file_imagen_extra2' in request.POST:
            investigacion.imagen_extra_2.delete()
            investigacion.imagen_extra_2 = None
            investigacion.save()

        if 'delete_file_imagen_extra3' in request.POST:
            investigacion.imagen_extra_3.delete()
            investigacion.imagen_extra_3 = None
            investigacion.save()

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Información actualizada correctamente')
            return redirect('investigacion')
        else:
            context = {
                'investigacion': investigacion,
                'form': form,
                'categorias': categorias,
                'form_errors': form.errors
            }
            return render(request, self.template_name, context)


# Vista para eliminar una investigacion


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser), name='dispatch')
class InvestigacionEliminarView(TemplateView):
    def get(self, request, nombre):
        investigacion = get_object_or_404(Investigacion, nombre=nombre)
        investigacion.delete()
        messages.success(
            request, 'La investigación ha sido eliminada correctamente')
        return redirect('investigacion')

# Vista para agregar una nueva investigacion


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser), name='dispatch')
class InvestigacionCreateView(TemplateView):
    template_name = "investigacion/investigacion_create.html"

    def get(self, request):
        form = InvestigacionForm()
        categorias = CategoriaI.objects.all()

        context = {
            'form': form,
            'categorias': categorias
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = InvestigacionForm(request.POST, request.FILES)
        categorias = CategoriaI.objects.all()

        if form.is_valid():
            form.save()
            messages.success(request, 'Investigación creada correctamente')
            return redirect('investigacion')
        else:
            context = {
                'form': form,
                'categorias': categorias,
                'form_errors': form.errors
            }
            return render(request, self.template_name, context)
