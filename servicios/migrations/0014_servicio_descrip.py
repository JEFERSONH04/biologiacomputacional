# Generated by Django 5.0.1 on 2024-03-10 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0013_alter_servicio_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='descrip',
            field=models.TextField(blank=True),
        ),
    ]
