# Generated by Django 5.0.1 on 2024-03-14 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investigacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigacion',
            name='imagen_tif',
            field=models.ImageField(blank=True, upload_to='investigacion-tif/'),
        ),
        migrations.AlterField(
            model_name='investigacion',
            name='mejores_pdf',
            field=models.FileField(blank=True, upload_to='investigacion-mejores/'),
        ),
        migrations.AlterField(
            model_name='investigacion',
            name='pdf',
            field=models.FileField(blank=True, upload_to='investigacion-pdf/'),
        ),
    ]