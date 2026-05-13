from django.db import models
from django.utils import timezone
# Create your models here.
class Compra(models.Model):
    numeroCompra = models.CharField(max_length = 200)
    fechaCompra = models.DateTimeField(default=timezone.now) #para que fecha sea la actual
    codigoPrenda = models.CharField(max_length = 200)
    nombrePrenda = models.CharField(max_length = 200)
    descripcionPrenda = models.TextField(max_length = 200)
    cantidadComprada = models.CharField(max_length = 200)
    precioNetoUnitario = models.CharField(max_length = 200)
    precioNetoTotal = models.CharField(max_length = 200)
    iva = models.CharField(max_length = 200, default=19)
    precioBrutoTotal = models.CharField(max_length = 200)
    medioDePago = models.CharField(max_length = 200)
    nombreProveedor = models.CharField(max_length = 200)
    direccionProveedor = models.CharField(max_length = 200)

    def __str__(self):
        return f"""
            {self.numeroCompra} | {self.fechaCompra} | {self.codigoPrenda} | {self.nombrePrenda} |
            {self.descripcionPrenda} | {self.cantidadComprada} | {self.precioNetoUnitario} |
            {self.precioNetoTotal} | {self.iva} | {self.precioBrutoTotal} | {self.medioDePago} |
            {self.nombreProveedor} | {self.direccionProveedor}
        """
    #Para que se calcule el precio bruto total
    def save(self, *args, **kwargs):
        if not self.precioNetoTotal:
            self.precioNetoTotal = self.cantidadComprada * self.precioNetoUnitario
            self.precioBrutoTotal = self.precioNetoTotal + self.precioNetoTotal * (self.iva)/100.0
        super().save(*args, **kwargs)