from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path("", views.index, name = "index"),
    path("formulario/", views.formulario, name="formulario"),
    path("<int:numeroCompra>/eliminar/", views.CompraDeleteView.as_view(), name="indexEliminarUnaCompra"),
    path("<int:numeroCompra>/<int:numeroPrenda>/momentanea/eliminar/", views.CompraDetalleMomentaneaDeleteView.as_view(), name="eliminarUnaCompraDetalleMomentanea"),
    path("eliminarTodasCompras/", views.eliminarTodasCompras, name="eliminarTodasCompras"),
]
