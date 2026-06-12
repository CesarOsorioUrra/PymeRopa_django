from django.db import models
from django.utils import timezone
from django.conf import settings
from inventario.models import Prenda, PrendaMomentanea

# Create your models here.
class Compra(models.Model):
    numeroCompra = models.IntegerField(primary_key=True)
    fechaCompra = models.DateTimeField(default=timezone.now) #para que fecha sea la actual
    iva = models.IntegerField(default=19)
    precioBrutoTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    medioDePago = models.CharField(max_length = 30)
    nombreProveedor = models.CharField(max_length = 100)
    direccionProveedor = models.CharField(max_length = 200)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    def __str__(self):
        return f"""
            {self.numeroCompra} | {self.fechaCompra} | {self.iva} | {self.precioBrutoTotal} | 
            {self.medioDePago} | {self.nombreProveedor} | {self.direccionProveedor} | {self.usuario}
        """

class CompraDetalle(models.Model):
    numeroCompra = models.ForeignKey(Compra, models.CASCADE)
    numeroPrenda = models.ForeignKey(Prenda, models.CASCADE)
    nombrePrenda = models.CharField(max_length = 100)
    descripcionPrenda = models.TextField(max_length = 200)
    cantidadComprada = models.IntegerField(default = 0)
    precioNetoUnitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precioNetoTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    pk = models.CompositePrimaryKey('numeroCompra', 'numeroPrenda')

    def __str__(self):
        return f"""
            {self.numeroCompra} | {self.numeroPrenda} | {self.nombrePrenda} | {self.descripcionPrenda} 
            | {self.cantidadComprada} | {self.precioNetoUnitario} | {self.precioNetoTotal}
        """

class CompraMomentanea(models.Model):
    numeroCompra = models.IntegerField(primary_key=True)
    fechaCompra = models.DateTimeField(default=timezone.now) #para que fecha sea la actual
    iva = models.IntegerField(default=19)
    precioBrutoTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    medioDePago = models.CharField(max_length = 30)
    nombreProveedor = models.CharField(max_length = 100)
    direccionProveedor = models.CharField(max_length = 200)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

class CompraDetalleMomentanea(models.Model):
    numeroCompra = models.ForeignKey(CompraMomentanea, models.CASCADE)
    numeroPrenda = models.ForeignKey(PrendaMomentanea, models.CASCADE)
    nombrePrenda = models.CharField(max_length = 100)
    descripcionPrenda = models.TextField(max_length = 200)
    cantidadComprada = models.IntegerField(default = 0)
    precioNetoUnitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precioNetoTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    pk = models.CompositePrimaryKey('numeroCompra', 'numeroPrenda')