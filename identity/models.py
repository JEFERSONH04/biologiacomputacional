from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class AdditionalUserInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('hombre', 'Hombre'), ('mujer', 'Mujer'), ('noBinario','NoBinario')], blank=False, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return 'Informacion adicional de %s' % (self.user)

class ProfileAdditionalInfo(models.Model):
    GENDER_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
        ('noBinario', 'Prefiero no decirlo'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    
    def __str__(self):
        return 'Informacion adicional del usuario %s' % (self.user)
    
class AdditionalUserInfoForm(forms.ModelForm):
    class Meta:
        model = AdditionalUserInfo
        fields = ['phone_number', 'image']