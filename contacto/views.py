from BiologiaComputacional.forms import FormularioContacto
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.


def contacto(request):
    if request.method == "POST":
        formulario = FormularioContacto(request.POST)
        if formulario.is_valid():
            infForm = formulario.cleaned_data
            message = "Nombre completo: " + infForm['nombres'] + " " + infForm['apellidos'] + "\nTelefono: " + \
                infForm['telefono'] + "\nOpiniones: " + \
                infForm['opiniones'] + "\nCorreo: " + infForm.get('email', '')
            send_mail('Información de contacto', message, settings.EMAIL_HOST_USER, [
                      'sinfoniadefragancias@gmail.com'],)
            messages.success(request, 'Formulario enviado correctamente')
            return redirect('inicio')
        else:
            messages.error(request, 'Hubo un error en el formulario. Por favor, revisa los campos e inténtalo de nuevo.')
    else:
        formulario = FormularioContacto()
    return render(request, "contacto/contacto.html", {"form": formulario})
