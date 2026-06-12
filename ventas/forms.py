from django import forms
from .models import Venta, VentaDetalle

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ["numeroVenta", "fechaVenta", "iva", "precioBrutoTotal", "medioDePago"]
        mediosDePago = (('Efectivo', 'Efectivo'), ('Tarjeta de credito', 'Tarjeta de credito'), 
                        ('Tarjeta de debito', 'Tarjeta de debito'), ('Transferencia', 'Transferencia'))
        widgets = {"medioDePago": forms.Select(choices=mediosDePago), "precioBrutoTotal": forms.NumberInput(attrs={'readonly': 'readonly'})}
        
class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = VentaDetalle
        fields = ["numeroPrenda", "cantidadVendida", "precioNetoUnitario", "precioNetoTotal"]
        widgets = {"precioNetoTotal": forms.NumberInput(attrs={'readonly': 'readonly'})}