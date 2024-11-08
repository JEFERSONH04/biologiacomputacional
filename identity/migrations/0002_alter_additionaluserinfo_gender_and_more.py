# Generated by Django 5.0.1 on 2024-01-31 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionaluserinfo',
            name='gender',
            field=models.CharField(choices=[('hombre', 'Hombre'), ('mujer', 'Mujer'), ('noBinario', 'NoBinario')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='additionaluserinfo',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='static/identity/images/profile'),
        ),
    ]
