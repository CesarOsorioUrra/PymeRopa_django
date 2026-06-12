from django import forms
from .models import Compra, CompraDetalle

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ["numeroCompra", "fechaCompra", "iva", "precioBrutoTotal", "medioDePago", 
                  "nombreProveedor", "direccionProveedor"
                  ]
        mediosDePago = (('Efectivo', 'Efectivo'), ('Tarjeta de credito', 'Tarjeta de credito'), 
                ('Tarjeta de debito', 'Tarjeta de debito'), ('Transferencia', 'Transferencia'))
        widgets = {"medioDePago": forms.Select(choices=mediosDePago), "precioBrutoTotal": forms.NumberInput(attrs={'readonly': 'readonly'})}
        
class CompraDetalleForm(forms.ModelForm):
    class Meta:
        model = CompraDetalle
        fields = ["nombrePrenda", "descripcionPrenda", "cantidadComprada",
                  "precioNetoUnitario", "precioNetoTotal"
                  ]
        widgets = {"precioNetoTotal": forms.NumberInput(attrs={'readonly': 'readonly'})}

class NumeroPrendaForm(forms.Form):
    numeroPrenda = forms.IntegerField(widget=forms.NumberInput())
