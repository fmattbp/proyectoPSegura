from django.contrib import admin
from .models import servers , client_server
# Register your models here.

@admin.register(servers,client_server)
class DefaultAdmin(admin.ModelAdmin):
    pass
