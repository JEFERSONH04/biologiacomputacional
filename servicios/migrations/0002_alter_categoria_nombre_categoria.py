# Generated by Django 5.0.1 on 2024-03-06 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nombre_categoria',
            field=models.CharField(max_length=20),
        ),
    ]
