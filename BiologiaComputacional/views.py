from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from identity.models import Tipografias


def inicio(request):
    tipografias = Tipografias.objects.all()
    context = {}

    if request.method == 'POST':
        fuente_titulo = request.POST.get('fuente_titulo', 'Arial')
        fuente_texto = request.POST.get('fuente_texto', 'Times New Roman')

        # Pasa los valores al contexto de la plantilla
        context['fuente_titulo'] = fuente_titulo
        context['fuente_texto'] = fuente_texto

        # Imprimir para depuración
        print("Datos POST:", request.POST)
        print(fuente_titulo)
        print(fuente_texto)

        return render(request, 'success.html', context)

    return render(request, 'inicio.html', {'tipografias': tipografias, **context})



def mi_vista_404(request, exception):
    return render(request, 'templates/404.html', status=404)

def view_403(request, exception=None):
    return render(request, 'templates/404.html', status=403)

class politicas_privacidad(TemplateView):
    
    template_name = "politicas_privacidad.html"