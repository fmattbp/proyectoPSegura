from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class IPs(models.Model):
    ip = models.GenericIPAddressField(null=False, blank=False, unique=True)
    ultima_peticion = models.DateTimeField(null=False, blank=False)
    intentos = models.IntegerField(null=False, blank=False, default=0)

class servers(models.Model):
    url_servicios = models.CharField(max_length=40,null=False, blank=False, unique=True,primary_key=True)
    nombre = models.CharField(max_length=10, null=True,blank=False, unique=True)

    def __str__(self):
        return self.url_servicios


class client_server(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    url_servicios = models.OneToOneField(servers,on_delete=models.CASCADE)

class registrar_contraseña(models.Model):
    usuario = models.CharField(max_length=20, null=False,blank=False, unique=True, primary_key=True)
    contraseña = models.CharField(max_length=50,null=False, blank=False)
