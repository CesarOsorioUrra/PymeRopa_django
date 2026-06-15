from django.db import models
from django.conf import settings
from django.utils import timezone
from inventario.models import Prenda
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Venta(models.Model):
    numeroVenta = models.AutoField(primary_key=True)
    fechaVenta = models.DateTimeField(default=timezone.now) #para que fecha sea la actual
    iva = models.IntegerField(default=19, validators = [MinValueValidator(0), MaxValueValidator(100)])
    precioBrutoTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators = [MinValueValidator(0)])
    medioDePago = models.CharField(max_length = 30)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    def __str__(self):
        return f"""
            {self.numeroVenta} | {self.fechaVenta} | {self.iva} | 
            {self.precioBrutoTotal} | {self.medioDePago} | {self.usuario}
        """
class VentaDetalle(models.Model):
    numeroVenta = models.ForeignKey(Venta, models.CASCADE, validators = [MinValueValidator(1)])
    numeroPrenda = models.ForeignKey(Prenda, models.CASCADE, validators = [MinValueValidator(1)]) #las FK por defecto apuntan a la PK de la clase referenciada
    cantidadVendida = models.IntegerField(default = 0, validators = [MinValueValidator(1)])
    precioNetoUnitario = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators = [MinValueValidator(0)])
    precioNetoTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators = [MinValueValidator(0)])

    pk = models.CompositePrimaryKey('numeroVenta', 'numeroPrenda')

    def __str__(self):
        return f"""
            {self.numeroVenta} | {self.numeroPrenda} | {self.cantidadVendida} | 
            {self.precioNetoUnitario} | {self.precioNetoTotal}
        """

class VentaMomentanea(models.Model):
    numeroVenta = models.AutoField(primary_key=True)
    fechaVenta = models.DateTimeField(default=timezone.now) #para que fecha sea la actual
    iva = models.IntegerField(default=19)
    precioBrutoTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    medioDePago = models.CharField(max_length = 30)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    def __str__(self):
        return f"""
            {self.numeroVenta} | {self.fechaVenta} | {self.iva} | 
            {self.precioBrutoTotal} | {self.medioDePago} | {self.usuario}
        """

class VentaDetalleMomentanea(models.Model):
    numeroVenta = models.ForeignKey(VentaMomentanea, models.CASCADE)
    numeroPrenda = models.ForeignKey(Prenda, models.CASCADE)
    cantidadVendida = models.IntegerField(default = 0)
    precioNetoUnitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precioNetoTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    pk = models.CompositePrimaryKey('numeroVenta', 'numeroPrenda')

    def __str__(self):
        return f"""
            {self.numeroVenta} | {self.numeroPrenda} | {self.cantidadVendida} | 
            {self.precioNetoUnitario} | {self.precioNetoTotal}
        """