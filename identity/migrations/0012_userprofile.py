# Generated by Django 5.0.4 on 2024-11-07 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0011_remove_additionaluserinfo_profile_picture_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('font_family', models.CharField(choices=[('Arial', 'Arial'), ('Times New Roman', 'Times New Roman'), ('Courier New', 'Courier New'), ('Georgia', 'Georgia'), ('Verdana', 'Verdana')], default='Arial', max_length=100)),
                ('font_size', models.CharField(default='16px', max_length=10)),
            ],
        ),
    ]
