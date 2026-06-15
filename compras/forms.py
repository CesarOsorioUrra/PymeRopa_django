from django import forms
from .models import CompraMomentanea, CompraDetalleMomentanea

class CompraForm(forms.ModelForm):
    class Meta:
        model = CompraMomentanea
        fields = ["fechaCompra", "iva", "precioBrutoTotal", "medioDePago", 
                  "nombreProveedor", "direccionProveedor"
                  ]
        mediosDePago = (('Efectivo', 'Efectivo'), ('Tarjeta de credito', 'Tarjeta de credito'), 
                ('Tarjeta de debito', 'Tarjeta de debito'), ('Transferencia', 'Transferencia'))
        widgets = {
            "iva": forms.NumberInput(attrs={'min' : '0', 'max' : '100'}),
            "precioBrutoTotal": forms.NumberInput(attrs={'readonly': 'readonly', 'min': '0'}),
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
        
class CompraDetalleForm(forms.ModelForm):
    class Meta:
        model = CompraDetalleMomentanea
        fields = ["nombrePrenda", "descripcionPrenda", "cantidadComprada",
                  "precioNetoUnitario", "precioNetoTotal"
                  ]
        widgets = {
            "cantidadComprada": forms.NumberInput(attrs={'min': '1'}),
            "precioNetoUnitario": forms.NumberInput(attrs={'min': '0'}),
            "precioNetoTotal": forms.NumberInput(attrs={'readonly': 'readonly', 'min': '0'})
            }
        def clean_cantidadComprada(self):
            cantidadComprada = self.cleaned_data.get('cantidadComprada')
            if cantidadComprada <= 0:
                raise forms.ValidationError("La cantidadComprada ingresada no puede ser negativa ni 0.")
            return cantidadComprada
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

class NumeroPrendaForm(forms.Form):
    numeroPrenda = forms.IntegerField(widget=forms.NumberInput(attrs={'min': '1'}))