# Generated by Django 5.0.1 on 2024-05-22 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0020_alter_servicio_desarrollador_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='nombre',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
