# Generated by Django 5.0.1 on 2024-03-07 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0007_servicio_autor_enlace'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='licencia',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='servicio',
            name='licencia_enlace',
            field=models.URLField(blank=True),
        ),
    ]