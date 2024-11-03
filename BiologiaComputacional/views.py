from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView



def inicio(request):

    return render(request, "inicio.html")

def mi_vista_404(request, exception):
    return render(request, 'templates/404.html', status=404)

def view_403(request, exception=None):
    return render(request, 'templates/404.html', status=403)

class politicas_privacidad(TemplateView):
    
    template_name = "politicas_privacidad.html"