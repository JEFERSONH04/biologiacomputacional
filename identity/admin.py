from django.contrib import admin
from identity.models import AdditionalUserInfo, ProfileAdditionalInfo

# Register your models here.

admin.site.register(AdditionalUserInfo)
admin.site.register(ProfileAdditionalInfo)