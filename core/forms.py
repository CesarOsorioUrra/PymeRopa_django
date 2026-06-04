from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class AvisoForm(forms.Form):
    usuario = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label="Seleccione los usuarios", widget=forms.CheckboxSelectMultiple)
    mensaje = forms.CharField(max_length = 200, widget=forms.Textarea())