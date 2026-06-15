from django import forms
from .models import VentaMomentanea, VentaDetalleMomentanea

class VentaForm(forms.ModelForm):
    class Meta:
        model = VentaMomentanea
        fields = ["fechaVenta", "iva", "precioBrutoTotal", "medioDePago"]
        mediosDePago = (('Efectivo', 'Efectivo'), ('Tarjeta de credito', 'Tarjeta de credito'), 
                        ('Tarjeta de debito', 'Tarjeta de debito'), ('Transferencia', 'Transferencia'))
        widgets = {
            "iva": forms.NumberInput(attrs={'min' : '0', 'max' : '100'}),
            "precioBrutoTotal": forms.NumberInput(attrs={'readonly': 'readonly', 'min' : '0'}),
            "medioDePago": forms.Select(choices=mediosDePago)
            }
        def clean_iva(self):
            iva = self.cleaned_data.get('iva')
            if iva < 0:
                raise forms.ValidationError("El iva ingresado no puede ser negativo.")
            elif iva > 100:
                raise forms.ValidationError("El iva ingresado no puede ser mayor a 100.")
            return iva
        def clean_precioBrutoTotal(self):
            precioBrutoTotal = self.cleaned_data.get('precioBrutoTotal')
            if precioBrutoTotal < 0:
                raise forms.ValidationError("El precioBrutoTotal ingresado no puede ser negativo.")
            return precioBrutoTotal

class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = VentaDetalleMomentanea
        fields = ["numeroPrenda", "cantidadVendida", "precioNetoUnitario", "precioNetoTotal"]
        widgets = {
            "cantidadVendida": forms.NumberInput(attrs={'min' : '1'}),
            "precioNetoUnitario": forms.NumberInput(attrs={'min' : '0'}),
            "precioNetoTotal": forms.NumberInput(attrs={'readonly': 'readonly', 'min' : '0'})
            }
        def clean_cantidadVendida(self):
            cantidadVendida = self.cleaned_data.get('cantidadVendida')
            if cantidadVendida <= 0:
                raise forms.ValidationError("La cantidadVendida ingresada no puede ser negativa ni 0.")
            return cantidadVendida
        def clean_precioNetoUnitario(self):
            precioNetoUnitario = self.cleaned_data.get('precioNetoUnitario')
            if precioNetoUnitario < 0:
                raise forms.ValidationError("El precioNetoUnitario ingresado no puede ser negativo.")
            return precioNetoUnitario
        def clean_precioNetoTotal(self):
            precioNetoTotal = self.cleaned_data.get('precioNetoTotal')
            if precioNetoTotal < 0:
                raise forms.ValidationError("El precioNetoTotal ingresado no puede ser negativo.")
            return precioNetoTotal