from django.contrib import admin
from .models import servers , client_server, registrar_contraseña
# Register your models here.

@admin.register(servers,client_server,registrar_contraseña)
class DefaultAdmin(admin.ModelAdmin):
    pass
