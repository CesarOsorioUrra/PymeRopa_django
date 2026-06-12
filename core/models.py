from django.db import models
from django.conf import settings
# Create your models here.

class InformacionUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE, primary_key=True)
    aviso = models.TextField(max_length=1000, null=True)
    salario = models.IntegerField(default=0)
