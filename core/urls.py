from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
app_name = 'core'

urlpatterns = [
    path("", views.home, name="home"),
    path("administracion/", views.administracion, name="administracion"),

    path("administracion/usuarios/", views.administracion_usuarios, name="administracion_usuarios"),
    path("administracion/usuarios/<int:id>/actualizar/", views.UserUpdateView.as_view(), name="administracion_usuariosActualizar"),
    path("administracion/usuarios/<int:id>/eliminar/", views.UserDeleteView.as_view(), name="administracion_usuariosEliminar"),

    path("administracion/prendas/", views.administracion_prendas, name="administracion_prendas"),
    path("administracion/prendas/<int:numeroPrenda>/actualizar/", views.PrendaUpdateView.as_view(), name="administracion_prendasActualizar"),
    path("administracion/prendas/<int:numeroPrenda>/eliminar/", views.PrendaDeleteView.as_view(), name="administracion_prendasEliminar"),

    path("administracion/compras/", views.administracion_compras, name="administracion_compras"),
    path("administracion/compras/<int:numeroCompra>/eliminar/", views.CompraDeleteView_Administracion.as_view(), name="administracion_comprasEliminar"),

    path("administracion/ventas/", views.administracion_ventas, name="administracion_ventas"),
    path("administracion/ventas/<int:numeroVenta>/eliminar/", views.VentaDeleteView_Administracion.as_view(), name="administracion_ventasEliminar"),

    path("administracion/informacionesUsuario/", views.administracion_informacionesUsuario, name="administracion_informacionesUsuario"),
    path("administracion/informacionesUsuario/<int:id>/actualizarSalario/", views.InformacionUsuarioUpdateView.as_view(), name="administracion_informacionesUsuarioActualizarSalario"),
    path("administracion/informacionesUsuario/<int:id>/eliminarAviso/", views.InformacionUsuarioEliminarAviso.as_view(), name="administracion_informacionesUsuarioEliminarAviso"),

    path("aviso/", views.aviso, name="aviso"),
    path("cuenta/login/", auth_views.LoginView.as_view(), name="login"), #voy a importar vista desde lo que ya me ofrece django
    path("cuenta/logout/", auth_views.LogoutView.as_view(), name="logout")
]
