from django.db import models

# Create your models here.

class Carrusel(models.Model):
    titulo = models.CharField(max_length=50, blank=True)
    texto1 = models.CharField(max_length=100, blank=False)
    texto2 = models.CharField(max_length=100, blank=False)
    texto3 = models.CharField(max_length=100, blank=False)
    imagen1 = models.ImageField(upload_to='imagen-carrusel-1/', blank=False)
    imagen2 = models.ImageField(upload_to='imagen-carrusel-2/', blank=False)
    imagen3 = models.ImageField(upload_to='imagen-carrusel-3/', blank=False)
    
    def __str__(self):
        return 'Datos carrusel de fotos'

class CategoriaI(models.Model):
    nombre_categoria = models.CharField(max_length=20, blank=False)
    
    def __str__(self):
        return 'Categoria de investigacion %s' % (self.nombre_categoria)
    
class Investigacion(models.Model):
    categoria = models.ForeignKey(CategoriaI, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, blank=False, unique=True)
    descrip = models.TextField(blank=False)
    imagen_investigacion = models.ImageField(upload_to='investigacion-imagenes/', blank=False)
    imagen_tif = models.ImageField(upload_to='investigacion-tif/', blank=True)
    pdf = models.FileField(upload_to='investigacion-pdf/', blank=True)
    mejores_pdf = models.FileField(upload_to='investigacion-mejores/', blank=True)
    imagen_extra_1 = models.ImageField(upload_to='investigacion-imagenes-extras1/', blank=True)
    imagen_extra_2 = models.ImageField(upload_to='investigacion-imagenes-extras2/', blank=True)
    imagen_extra_3 = models.ImageField(upload_to='investigacion-imagenes-extras3/', blank=True)
    
    def __str__(self):
        if self.categoria.nombre_categoria == 'Alpha':
            return 'PROYECTO ALPHA-SINUCLEINA %s' % self.nombre
        elif self.categoria.nombre_categoria == 'Cry11':
            return 'FAMILIA CRY11 %s' % self.nombre
        elif self.categoria.nombre_categoria == 'Otros':
            return 'Otros %s' % self.nombre
        else:
            return self.nombre