from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path("", views.index, name = "index"),
    path("formulario/", views.formulario, name="formulario"),
    path("<int:numeroVenta>/eliminar/", views.VentaDeleteView.as_view(), name="indexEliminarUnaVenta"),
    path("<int:numeroVenta>/<int:numeroPrenda>/momentanea/eliminar/", views.VentaDetalleMomentaneaDeleteView.as_view(), name="eliminarUnaVentaDetalleMomentanea"),
    path("eliminarTodasVentas/", views.eliminarTodasVentas, name="eliminarTodasVentas"),
]
