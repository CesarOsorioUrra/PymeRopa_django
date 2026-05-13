from django.db import models

# Create your models here.
class Inventario(models.Model):
    codigoPrenda = models.CharField(max_length = 200)
    nombrePrenda = models.CharField(max_length = 200)
    descripcionPrenda = models.TextField(max_length = 200)
    cantidad = models.CharField(max_length = 200)
    precioNetoUnitario = models.CharField(max_length = 200)

    def __str__(self):
        return f"""
            {self.codigoPrenda} | {self.nombrePrenda} |
            {self.descripcionPrenda} | {self.cantidad} | {self.precioNetoUnitario}
        """