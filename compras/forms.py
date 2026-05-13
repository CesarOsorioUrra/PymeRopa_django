from django import forms
from .models import Compra

class ComprasForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ["numeroCompra", "fechaCompra", "codigoPrenda", "nombrePrenda", "descripcionPrenda", "cantidadComprada", 
                  "precioNetoUnitario", "precioNetoTotal", "iva", "precioBrutoTotal", "medioDePago", 
                  "nombreProveedor", "direccionProveedor"
                  ]

