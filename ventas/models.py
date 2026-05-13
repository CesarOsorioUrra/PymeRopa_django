from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
class Venta(models.Model):
    numeroVenta = models.CharField(max_length = 200)
    fechaVenta = models.DateTimeField(default=timezone.now) #para que fecha sea la actual
    codigoPrenda = models.CharField(max_length = 200)
    nombrePrenda = models.CharField(max_length = 200)
    descripcionPrenda = models.TextField(max_length = 200)
    cantidadVendida = models.CharField(max_length = 200)
    precioNetoUnitario = models.CharField(max_length = 200)
    precioNetoTotal = models.CharField(max_length = 200)
    iva = models.CharField(max_length = 200, default=19)
    precioBrutoTotal = models.CharField(max_length = 200)
    medioDePago = models.CharField(max_length = 200)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, default=1)
    def __str__(self):
        return f"""
            {self.numeroVenta} | {self.fechaVenta} | {self.codigoPrenda} | {self.nombrePrenda} |
            {self.descripcionPrenda} | {self.cantidadVendida} | {self.precioNetoUnitario} |
            {self.precioNetoTotal} | {self.iva} | {self.precioBrutoTotal} | {self.medioDePago} |

        """
    #Para que se calcule el precio bruto total
    def save(self, *args, **kwargs):
        if not self.precioNetoTotal:
            self.precioNetoTotal = self.cantidadVendida * self.precioNetoUnitario
            self.precioBrutoTotal = self.precioNetoTotal + self.precioNetoTotal * (self.iva)/100.0
        super().save(*args, **kwargs)