from django import forms
from .models import Venta

class VentasForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ["numeroVenta", "fechaVenta", "codigoPrenda", "nombrePrenda", "descripcionPrenda", "cantidadVendida", 
                  "precioNetoUnitario", "precioNetoTotal", "iva", "precioBrutoTotal", "medioDePago"
                  ]
        