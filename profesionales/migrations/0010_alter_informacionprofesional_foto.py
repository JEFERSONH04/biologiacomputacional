# Generated by Django 5.0.1 on 2024-02-03 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0009_alter_informacionprofesional_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informacionprofesional',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]