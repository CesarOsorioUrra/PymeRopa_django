from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path("", views.index, name = "index"),
    path("formulario/", views.formulario, name="formulario")
]
