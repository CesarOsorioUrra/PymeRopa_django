from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AvisoForm, UserForm, PrendaForm, InformacionUsuarioForm
from django.contrib import messages
from .models import InformacionUsuario
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from inventario.models import Prenda
from compras.models import Compra, CompraDetalle
from ventas.models import Venta, VentaDetalle
from .models import InformacionUsuario
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import RedirectView

#Pagina de inicio, al ser visitada por un usuario, se le creará un registro de informacion usuario para ese usuario
#Este registro se crea en caso de no existir.
#Este registro de informaciones de usuario sirve para poder almacenar y mostrar los salarios y avisos de cada empleado.
def home(request):
    if request.user.is_authenticated:
        existeInformacionUsuario = InformacionUsuario.objects.filter(usuario = request.user.id).exists()
        if not existeInformacionUsuario:
            informacionUsuario = InformacionUsuario()
            informacionUsuario.usuario = request.user
            informacionUsuario.save()
        aviso = InformacionUsuario.objects.get(usuario = request.user.id).aviso
        salario = InformacionUsuario.objects.get(usuario = request.user.id).salario
    else:
        aviso = None
        salario = None
    context = {"aviso": aviso, "salario": salario}
    return render(request, 'core/home.html', context)

@user_passes_test(lambda usuario: usuario.is_superuser)
@login_required
def administracion(request):
    return render(request, 'core/administracion.html')

#Logica para poder crear un usuario en la pagina de administracion
@user_passes_test(lambda usuario: usuario.is_superuser)
@login_required
def administracion_usuarios(request):
    UserModel = get_user_model()
    usuarios = UserModel.objects.all()
    if request.POST:
        formUsuario = UserForm(request.POST)
        if formUsuario.is_valid():
            usuario = UserModel()
            usuario.username = formUsuario.cleaned_data.get('username')
            usuario.first_name = formUsuario.cleaned_data.get('first_name')
            usuario.last_name = formUsuario.cleaned_data.get('last_name')
            usuario.email = formUsuario.cleaned_data.get('email')
            usuario.is_superuser = formUsuario.cleaned_data.get('is_superuser')
            usuario.is_staff = formUsuario.cleaned_data.get('is_staff')
            usuario.is_active  = formUsuario.cleaned_data.get('is_active')
            usuario = formUsuario.save(commit=False) #se crea la instancia de usuario pero no se guarda en db todavia
            usuario.set_password(formUsuario.cleaned_data['password'])
            usuario.save()

            #al crear un usuario tambien se debe crear su informacion
            informacionUsuario = InformacionUsuario()
            informacionUsuario.usuario = usuario
            informacionUsuario.save()

            messages.success(request, "Usuario creado.")
            return redirect("core:administracion_usuarios")
    else:
        formUsuario = UserForm()
    context = {"renderizarUsuarios": True, "usuarios": usuarios, "formUsuario": formUsuario}
    return render(request, 'core/panelAdministracion.html', context)

#Vista generica para poder actualizar un usuario, para esto se debe pasar su id como parametro en la url
class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    UserModel = get_user_model()
    model = UserModel
    form_class = UserForm
    pk_url_kwarg = 'id' #se usa esto para que la url busque 'id' en lugar de 'pk'
    success_url = reverse_lazy('core:administracion_usuarios')
    success_message = "Usuario actualizado correctamente."
    def test_func(self): #esto se hace para ver si es super usuario
        return self.request.user.is_superuser
    #se debe sobreescribir este metodo para poder encriptar la contraseña del usuario al actualizar
    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        if password:
            user.set_password(password)
        user.save()
        return super().form_valid(form)

#Vista generica para poder eliminar un usuario, se debe pasar su id mediante la url
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    UserModel = get_user_model()
    model = UserModel
    pk_url_kwarg = 'id' #se usa esto para que la url busque 'id' en lugar de 'pk'
    success_url = reverse_lazy('core:administracion_usuarios')
    success_message = "Usuario eliminado correctamente."
    def test_func(self): #esto se hace para ver si es super usuario
        return self.request.user.is_superuser

@user_passes_test(lambda usuario: usuario.is_superuser)
@login_required
def administracion_prendas(request):
    prendas = Prenda.objects.all()
    context = {"renderizarPrendas": True, "prendas": prendas, "administracion": True}
    return render(request, 'core/panelAdministracion.html', context)

#Vista generica para actualizar prenda, se pasa su numeroPrenda por la url
class PrendaUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Prenda
    form_class = PrendaForm
    pk_url_kwarg = 'numeroPrenda' #se usa esto para que la url busque 'numeroPrenda' en lugar de 'pk'
    success_url = reverse_lazy('core:administracion_prendas')
    success_message = "Prenda actualizada correctamente."
    def test_func(self): #esto se hace para ver si es super usuario
        return self.request.user.is_superuser

#Vista generica para eliminar una prenda, se pasa su numeroPrenda por la url
class PrendaDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Prenda
    pk_url_kwarg = 'numeroPrenda' #se usa esto para que la url busque 'numeroPrenda' en lugar de 'pk'
    success_url = reverse_lazy('core:administracion_prendas')
    success_message = "Prenda eliminada correctamente."
    def test_func(self): #esto se hace para ver si es super usuario
        return self.request.user.is_superuser

@user_passes_test(lambda usuario: usuario.is_superuser)
@login_required
def administracion_compras(request):
    compras = Compra.objects.all()
    comprasDetalle = CompraDetalle.objects.all()
    context = {"renderizarCompras": True, "compras": compras, "comprasDetalle": comprasDetalle, "administracion": True}
    return render(request, 'core/panelAdministracion.html', context)

#Vista generica para eliminar una compra y sus detalles, se pasa su numeroCompra por la url
class CompraDeleteView_Administracion(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Compra
    pk_url_kwarg = 'numeroCompra' #se usa esto para que la url busque 'numeroCompra' en lugar de 'pk'
    success_url = reverse_lazy('core:administracion_compras')
    success_message = "Compra eliminada correctamente."
    def test_func(self): #esto se hace para ver si es super usuario
        return self.request.user.is_superuser

@user_passes_test(lambda usuario: usuario.is_superuser)
@login_required
def administracion_ventas(request):
    ventas = Venta.objects.all()
    ventasDetalle = VentaDetalle.objects.all()
    context = {"renderizarVentas": True, "ventas": ventas, "ventasDetalle": ventasDetalle, "administracion": True}
    return render(request, 'core/panelAdministracion.html', context)

#Vista generica para eliminar una venta, se pasa pasa su numeroVenta por la url
class VentaDeleteView_Administracion(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Venta
    pk_url_kwarg = 'numeroVenta' #se usa esto para que la url busque 'numeroVenta' en lugar de 'pk'
    success_url = reverse_lazy('core:administracion_ventas')
    success_message = "Venta eliminada correctamente."
    def test_func(self): #esto se hace para ver si es super usuario
        return self.request.user.is_superuser

@user_passes_test(lambda usuario: usuario.is_superuser)
@login_required
def administracion_informacionesUsuario(request):
    informacionesUsuario = InformacionUsuario.objects.all()
    context = {"renderizarInformacionesUsuario": True, "informacionesUsuario": informacionesUsuario}
    return render(request, 'core/panelAdministracion.html', context)

#Vista generica para poder actualizar el salario de un empleado
class InformacionUsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = InformacionUsuario
    form_class = InformacionUsuarioForm
    pk_url_kwarg = 'id' #se usa esto para que la url busque 'id' en lugar de 'pk'
    success_url = reverse_lazy('core:administracion_informacionesUsuario')
    success_message = "Información de usuario actualizada correctamente."
    def test_func(self): #esto se hace para ver si es super usuario
        return self.request.user.is_superuser

#Vista generica 'RedirectView' que se usa para poner el aviso de un usuario como None, y luego redirecciona a la misma pagina
class InformacionUsuarioEliminarAviso(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, RedirectView):
    pk_url_kwarg = 'id' #se usa esto para que la url busque 'id' en lugar de 'pk'
    success_message = "Aviso eliminado correctamente correctamente."
    pattern_name = reverse_lazy("core:administracion_informacionesUsuario") #pattern_name es la direccion de destino

    def test_func(self): #esto se hace para ver si es super usuario
        return self.request.user.is_superuser
    
    def get_redirect_url(self, *args, **kwargs):
        informacionUsuario = InformacionUsuario.objects.get(usuario = kwargs['id'])
        informacionUsuario.aviso = None
        informacionUsuario.save()
        return reverse_lazy("core:administracion_informacionesUsuario")
        
#Logic de formulario para publicar avisos
@user_passes_test(lambda usuario: usuario.is_superuser)
@login_required
def aviso(request):
    if request.POST:
        formAviso = AvisoForm(request.POST)
        if formAviso.is_valid():
            mensaje = formAviso.cleaned_data.get("mensaje")
            usuarios = formAviso.cleaned_data.get("usuarios") #son checkboxes

            for usuario in usuarios:
                informacionUsuario = InformacionUsuario.objects.filter(usuario = usuario).first() #first() para que sea una instancia y no un queryset
                informacionUsuario.aviso = mensaje
                informacionUsuario.save()
            
            usuarios_lista = list(usuarios)
            usuarios_lista_str = [str(usuario) for usuario in usuarios_lista]
            usuarios_lista_str_unida = ", ".join(usuarios_lista_str)

            messages.success(request, f"Aviso publicado correctamente. Usuarios: {usuarios_lista_str_unida}")
            return redirect("core:aviso")
    else:
        formAviso = AvisoForm()
    context = {"formAviso" : formAviso}
    return render(request, 'core/aviso.html', context)