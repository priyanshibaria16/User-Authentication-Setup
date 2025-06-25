from django.contrib import admin
from .models import *
# Register your models here.

class regi_(admin.ModelAdmin):
     list_display=('username','email')
admin.site.register(register,regi_)

class ad_(admin.ModelAdmin):
     list_display=('username','email')
admin.site.register(adregister,ad_)

admin.site.register(OTP)
admin.site.register(AdminOTP)



