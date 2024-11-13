from django.contrib import admin
from identity.models import AdditionalUserInfo, ProfileAdditionalInfo, Tipografias

# Register your models here.

admin.site.register(AdditionalUserInfo)
admin.site.register(ProfileAdditionalInfo)
admin.site.register(Tipografias)