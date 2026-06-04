from django.db import models
from django.conf import settings

# Create your models here.
class Prenda(models.Model):
    numeroPrenda = models.IntegerField(primary_key=True)
    nombrePrenda = models.CharField(max_length = 100)
    descripcionPrenda = models.TextField(max_length = 200)
    cantidad = models.IntegerField(default=0)
    precioNetoUnitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"""
            {self.numeroPrenda} | {self.nombrePrenda} |
            {self.descripcionPrenda} | {self.cantidad} | {self.precioNetoUnitario}
        """

class PrendaMomentanea(models.Model):
    numeroPrenda = models.IntegerField(primary_key=True)
    nombrePrenda = models.CharField(max_length = 100)
    descripcionPrenda = models.TextField(max_length = 200)
    cantidad = models.IntegerField(default=0)
    precioNetoUnitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, default=1) #Para que se pueda saber el usuario que esta comprando

    def __str__(self):
        return f"""
            {self.numeroPrenda} | {self.nombrePrenda} |
            {self.descripcionPrenda} | {self.cantidad} | {self.precioNetoUnitario} | {self.usuario}
        """