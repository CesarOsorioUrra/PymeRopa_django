from django import forms
from django.contrib.auth import get_user_model
from inventario.models import Prenda
from .models import InformacionUsuario

UserModel = get_user_model()

class AvisoForm(forms.Form):
    usuarios = forms.ModelMultipleChoiceField(queryset=UserModel.objects.all(), label="Seleccione los usuarios", widget=forms.CheckboxSelectMultiple)
    mensaje = forms.CharField(max_length = 1000, widget=forms.Textarea())

class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["username", "password", "first_name", "last_name", "email", "is_superuser", "is_staff", "is_active"]
        widgets = {'password': forms.PasswordInput()}

class PrendaForm(forms.ModelForm):
    class Meta:
        model = Prenda
        fields = ["nombrePrenda", "descripcionPrenda", "precioNetoUnitario"]

class InformacionUsuarioForm(forms.ModelForm):
    class Meta:
        model = InformacionUsuario
        fields = ["salario"]
        def clean_salario(self): #para validar que salario no sea menor a 0
            salario = self.cleaned_data.get('salario')
            if salario < 0:
                raise forms.ValidationError("El salario ingresado no puede ser negativo.")
            return salario




