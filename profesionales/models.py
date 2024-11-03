from django.db import models

# Create your models here.

class InformacionProfesional(models.Model):

    enlace_a_scholar = models.TextField(blank=True)
    foto = models.ImageField(upload_to='', blank=True, null=True)
    nombre = models.CharField(max_length = 30)
    apellido = models.CharField(max_length = 30)
    titulo_universitario = models.CharField(max_length = 30)
    universidad = models.CharField(max_length = 50, null=False, default='Unknown')
    email = models.EmailField()
    telefono = models.CharField(max_length = 10)
    campo0 = models.CharField(max_length=50, blank=True)
    campo1 = models.CharField(max_length=50, blank=True)
    campo2 = models.CharField(max_length=50, blank=True)
    campo3 = models.CharField(max_length=50, blank=True)
    campo4 = models.CharField(max_length=50, blank=True)
    campo5 = models.CharField(max_length=50, blank=True)
    campo6 = models.CharField(max_length=50, blank=True)
    facultad = models.CharField(max_length=35, blank=True)
    grupo_investigacion = models.CharField(max_length=35, blank=True)
    campus = models.CharField(max_length=35, blank=True)

    def __str__(self):
        return 'Informacion del profesional %s' % (self.nombre)
    
class Articulos(models.Model):
    
    profesional = models.ForeignKey(InformacionProfesional, on_delete=models.CASCADE)
    enlace_articulo = models.TextField(blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    anio = models.CharField(max_length=4)
    
    def __str__(self):
        return 'Relacion uno a muchos para InformacionProfesional'