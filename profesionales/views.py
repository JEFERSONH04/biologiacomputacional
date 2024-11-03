from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from profesionales.models import InformacionProfesional, Articulos
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from BiologiaComputacional.forms import FormularioContacto, ProfileFormProfessional, ArticleForm
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.forms.formsets import formset_factory
from django.forms import BaseFormSet
from django.core.exceptions import ValidationError
from django.http import request
from django.db import transaction
from django.urls import reverse


class busquedaInformacion(TemplateView):

    template_name = "profesionales/busquedaProfesional.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profesionales'] = InformacionProfesional.objects.all()
        return context


# Metodos para admin o staff


def is_superuser(user):

    return user.is_superuser


def is_staff(user):

    return user.is_staff


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff_or_superuser)
def agregar_profesional(request):
    campos = ['campo0', 'campo1', 'campo2',
              'campo3', 'campo4', 'campo5', 'campo6']
    
    ArticleFormSet = modelformset_factory(Articulos, form=ArticleForm, extra=1)

    if request.method == 'POST':
        prof_form = ProfileFormProfessional(request.POST, request.FILES)
        formset = ArticleFormSet(request.POST)

        if prof_form.is_valid() and formset.is_valid():
            nuevo_prof = prof_form.save(commit=False)
            nuevo_prof.nombre = nuevo_prof.nombre.capitalize()
            nuevo_prof.apellido = nuevo_prof.apellido.capitalize()
            nuevo_prof.titulo_universitario = nuevo_prof.titulo_universitario.capitalize()
            nuevo_prof.universidad = nuevo_prof.universidad.capitalize()
            nuevo_prof.campo0 = nuevo_prof.campo0.capitalize()
            nuevo_prof.campo1 = nuevo_prof.campo1.capitalize()
            nuevo_prof.campo2 = nuevo_prof.campo2.capitalize()
            nuevo_prof.campo3 = nuevo_prof.campo3.capitalize()
            nuevo_prof.campo4 = nuevo_prof.campo4.capitalize()
            nuevo_prof.campo5 = nuevo_prof.campo5.capitalize()
            nuevo_prof.campo6 = nuevo_prof.campo6.capitalize()
            nuevo_prof.facultad = nuevo_prof.facultad.capitalize()
            nuevo_prof.grupo_investigacion = nuevo_prof.grupo_investigacion.capitalize()
            nuevo_prof.campus = nuevo_prof.campus.capitalize()
            nuevo_prof.save()
            
            instances = formset.save(commit=False)
            for instance in instances:
                instance.profesional = nuevo_prof
                instance.save()

            messages.success(request, 'Profesional agregado correctamente')
            return redirect('buscarProfesional')
        else:
            messages.error(request, 'Errores en el formulario',
                           extra_tags='NoMostrar')

    else:
        prof_form = ProfileFormProfessional()
        formset = ArticleFormSet(queryset=Articulos.objects.none())

    return render(request, 'profesionales/agregarProfesional.html', {
        'form': prof_form,
        'formset': formset,
        'campos': campos,
    })


def info_profesional(request):
    info_pro = list(InformacionProfesional.objects.values())
    data = {'info_pro': info_pro}
    return JsonResponse(data, safe=False)


def detalle_profesional(request, pk):
    profesional = get_object_or_404(InformacionProfesional, pk=pk)
    articulos = profesional.articulos_set.all()

    try:
        prev_profesional = InformacionProfesional.objects.filter(
            nombre__lt=profesional.nombre).order_by('-nombre').first()
        next_profesional = InformacionProfesional.objects.filter(
            nombre__gt=profesional.nombre).order_by('nombre').first()
    except InformacionProfesional.DoesNotExist:
        prev_profesional = next_profesional = None

    return render(request, 'profesionales/detalle_profesional.html', {
        'profesional': profesional,
        'articulos': articulos,
        'prev_profesional': prev_profesional,
        'next_profesional': next_profesional
    })


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_superuser), name='dispatch')
class editar_profesional_view(UpdateView):
    model = InformacionProfesional
    form_class = ProfileFormProfessional
    template_name = 'profesionales/editar_profesional.html'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('detalle_profesional', kwargs={'pk': pk})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        ArticleFormSet = modelformset_factory(
            Articulos, form=ArticleForm, extra=1)
        formset = ArticleFormSet(
            request.POST, queryset=Articulos.objects.filter(profesional=self.object))

        if form.is_valid() and formset.is_valid():
            # Primero, eliminar los artículos seleccionados para eliminación
            articulo_ids = request.POST.getlist('eliminar_articulo')
            if articulo_ids:
                articulos_a_eliminar = Articulos.objects.filter(
                    id__in=articulo_ids)
                if articulos_a_eliminar.exists():
                    articulos_a_eliminar.delete()
                    messages.success(
                        request, 'Artículos eliminados correctamente.')
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        instances = formset.save(commit=False)
        for instance in instances:
            instance.profesional = self.object
            instance.save()
        formset.save_m2m()
        messages.success(self.request, 'Datos actualizados correctamente.')
        return redirect(self.get_success_url())

    def form_invalid(self, form, formset):
        messages.error(self.request, 'Fallo en la validación del formulario.')
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ArticleFormSet = modelformset_factory(
            Articulos, form=ArticleForm, extra=1)
        profesional = self.object
        context['profesional'] = profesional

        campos = {f'campo{i}': getattr(
            profesional, f'campo{i}', None) for i in range(7)}
        context['campos'] = campos

        if self.request.POST:
            context['formset'] = ArticleFormSet(self.request.POST)
        else:
            context['formset'] = ArticleFormSet(
                queryset=Articulos.objects.filter(profesional=self.object))

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_superuser), name='dispatch')
class eliminar_profesional_view(DeleteView):
    model = InformacionProfesional
    template_name = 'profesionales/eliminar_profesional.html'
    success_url = reverse_lazy('buscarProfesional')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profesional'] = self.object
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Profesional eliminado correctamente')
        return super().delete(request, *args, **kwargs)
