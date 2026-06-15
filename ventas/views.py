from django.shortcuts import render, redirect
from .models import Venta, VentaDetalle, VentaMomentanea, VentaDetalleMomentanea
from django.contrib.auth.decorators import login_required
from .forms import VentaForm, VentaDetalleForm
from django.contrib import messages
from inventario.models import Prenda
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.cache import cache

#Pagina index de ventas, en donde solo se muestran las ventas que ha realizado el usuario que esta logeado
#En esta pagina se podrá eliminar todas, o una, de las ventas que haya realizado el empleado logeado, para lo cual se pedira una confirmacion
@user_passes_test(lambda usuario: not usuario.is_superuser)
@login_required
def index(request):
    if request.POST:
        action = request.POST.get("action") #para chequear en que botón se hizo click
        if action == 'Eliminar':
            return redirect("ventas:eliminarTodasVentas")
        
    ventas = Venta.objects.filter(usuario = request.user) #Para que el empleado pueda ver solo sus ventas
    ventasDetalle = VentaDetalle.objects.filter(numeroVenta__usuario = request.user) #Para mostrar solo los detalles de venta de las ventas realizadas por el empleado actual

    context = {"ventas" : ventas, "ventasDetalle": ventasDetalle, "index": True}
    return render(request, "ventas/index.html", context)

#Vista para eliminar todas las ventas que haya registrado el usuario actual
@user_passes_test(lambda usuario: not usuario.is_superuser)
@login_required
def eliminarTodasVentas(request):
    if request.POST:
        Venta.objects.filter(usuario = request.user).delete()
        messages.success(request, "Sus ventas han sido eliminadas")
        return redirect("ventas:index")
    return render(request, "ventas/eliminarTodasVentas.html")

#Vista generica para eliminar definitivamente una venta que haya sido registrada por el usuario
class VentaDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Venta
    success_url = reverse_lazy('ventas:index')
    success_message = "Venta eliminada correctamente."
    pk_url_kwarg = 'numeroVenta' #se usa esto para que la url busque 'numeroVenta' en lugar de 'pk'
    def get_queryset(self):
        return Venta.objects.filter(usuario = self.request.user)
    def test_func(self): #esto se hace para ver si es super usuario
        return not self.request.user.is_superuser #ventas son realizadas por los no superusuarios

#Vista generica para eliminar un detalle de venta de una venta en curso
class VentaDetalleMomentaneaDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = VentaDetalleMomentanea
    success_url = reverse_lazy('ventas:formulario')
    success_message = "Detalle de venta eliminado correctamente."
    def get_queryset(self):
        return VentaDetalleMomentanea.objects.filter(numeroVenta__usuario = self.request.user)
    def test_func(self): #esto se hace para ver si es super usuario
        return not self.request.user.is_superuser #ventas son realizadas por los no superusuarios
    #se sobreescribe el metodo get_object() para asi poder recibir dos pks desde la url, esto ya que VentaDetalleMomentanea tiene una pk compuesta por dos pks, que ademas son FKs de VentaMomentanea
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        numeroVenta = self.kwargs.get('numeroVenta')
        numeroPrenda = self.kwargs.get('numeroPrenda')
        return get_object_or_404(queryset, numeroVenta = numeroVenta, numeroPrenda = numeroPrenda)
        
@user_passes_test(lambda usuario: not usuario.is_superuser)
@login_required
def formulario(request):
    ventasMomentaneas = VentaMomentanea.objects.filter(usuario = request.user)
    ventasDetalleMomentaneas = VentaDetalleMomentanea.objects.filter(numeroVenta__usuario = request.user)

    if request.POST:
        formVenta = VentaForm(request.POST)
        formVentaDetalle = VentaDetalleForm(request.POST)
        
        action = request.POST.get("action") #para chequear en que botón se hizo click
        
        if action == 'Agregar':
            if formVenta.is_valid() and formVentaDetalle.is_valid():

                #Realizacion de validaciones en el servidor para que ciertos valores no sean negativos o cero
                if formVentaDetalle.cleaned_data.get("numeroPrenda").numeroPrenda <= 0:
                    messages.error(request, "El numero de prenda no puede ser un número negativo, ni cero.")
                    return redirect("ventas:formulario") 
                if formVentaDetalle.cleaned_data.get("cantidadVendida") <= 0:
                    messages.error(request, "La cantidad vendida no puede ser un número negativo, ni cero.")
                    return redirect("ventas:formulario") 
                if formVentaDetalle.cleaned_data.get("precioNetoUnitario") < 0:
                    messages.error(request, "El precio neto unitario no puede ser un número negativo.")
                    return redirect("ventas:formulario") 
                if formVentaDetalle.cleaned_data.get("precioNetoTotal") < 0:
                    messages.error(request, "El precio neto total no puede ser un número negativo.")
                    return redirect("ventas:formulario") 
                if formVenta.cleaned_data.get("precioBrutoTotal") < 0:
                    messages.error(request, "El precio bruto total no puede ser un número negativo.")
                    return redirect("ventas:formulario") 
                
                numeroPrenda = formVentaDetalle.cleaned_data.get("numeroPrenda").numeroPrenda
                cantidadVendida = formVentaDetalle.cleaned_data.get("cantidadVendida")
                cantidadPrenda = Prenda.objects.filter(numeroPrenda = numeroPrenda).first().cantidad # .first() para que sea una instancia y no un queryset
                
                #Se verifica que no se venda mas cantidad de prenda de lo que se tiene en el inventario
                if cantidadVendida > cantidadPrenda:
                    messages.error(request, f"""No puede vender mayor cantidad de prendas de las que se tiene. En
                                     el inventario se tiene {cantidadPrenda} unidades, pero usted puso {cantidadVendida} unidades.""")
                    return redirect("ventas:formulario")

                #Se debe guardar y obtener el numero de venta en curso en el cache, para que los detalles de venta correspondan a la misma venta
                llave = 'numeroVentaEnCache'
                numeroVentaEnCache = cache.get(llave)

                #Si no está en el cache el numero de venta entonces se crea la instancia de ventaMomentanea (venta en curso)...
                #... y luego se agrega su numero de venta al cache, para que luego este numero de venta sea compartido por...
                #... los detalles de venta de esta orden de venta
                if numeroVentaEnCache is None:
                    ventaMomentanea = VentaMomentanea()
                    ventaMomentanea.numeroVenta = formVenta.cleaned_data.get("numeroVenta")
                    ventaMomentanea.fechaVenta = formVenta.cleaned_data.get("fechaVenta")
                    ventaMomentanea.iva = formVenta.cleaned_data.get("iva")
                    ventaMomentanea.precioBrutoTotal = formVenta.cleaned_data.get("precioBrutoTotal")
                    ventaMomentanea.medioDePago = formVenta.cleaned_data.get("medioDePago")
                    ventaMomentanea.usuario = request.user
                    ventaMomentanea.save()
                    cache.set(llave, ventaMomentanea.numeroVenta) #se guarda en cache el numero de venta de la venta en curso

                numeroVentaEnCache = cache.get(llave) #se obtiene del cache el numero de venta de la venta en curso
                ventaMomentanea = VentaMomentanea.objects.filter(numeroVenta = numeroVentaEnCache).first() #first() para que sea una intancia y no un queryset

                ventaDetalleMomentanea = VentaDetalleMomentanea()
                ventaDetalleMomentanea.numeroVenta = ventaMomentanea
                ventaDetalleMomentanea.numeroPrenda = formVentaDetalle.cleaned_data.get("numeroPrenda")
                ventaDetalleMomentanea.cantidadVendida = formVentaDetalle.cleaned_data.get("cantidadVendida")
                ventaDetalleMomentanea.precioNetoUnitario = formVentaDetalle.cleaned_data.get("precioNetoUnitario")
                ventaDetalleMomentanea.precioNetoTotal = formVentaDetalle.cleaned_data.get("precioNetoTotal")

                ventaDetalleMomentanea.save() #se guarda el detalle de la venta en curso

                messages.success(request, "Venta agregada a orden de venta")
                return redirect("ventas:formulario")
            
        elif action == 'Eliminar':
            VentaMomentanea.objects.filter(usuario = request.user).delete()
            llave = 'numeroVentaEnCache' #Al eliminar la orden de venta, se elimina del cache el numero de venta de la orden de venta en curso
            cache.delete(llave)

            messages.success(request, "Su orden de venta ha sido eliminada")
            return redirect("ventas:formulario") 
        
        #El boton para registrar ignora validaciones de los inputs del formulario en el cliente y en el servidor
        elif action == 'Registrar':
            #Debe checkearse que se haya ingresado una orden de venta antes de registrar
            if ventasMomentaneas.exists() == False:
                messages.error(request, "Debe ingresar una orden de venta.")
                return redirect("ventas:formulario")            
            #Debe checkearse que la orden de venta tenga detalles antes de registrar
            if ventasDetalleMomentaneas.exists() == False:
                messages.error(request, "La orden de venta debe tener al menos un detalle.")
                return redirect("ventas:formulario")

            for ventaMomentanea in ventasMomentaneas:
                venta = Venta()
                venta.numeroVenta = ventaMomentanea.numeroVenta
                venta.fechaVenta = ventaMomentanea.fechaVenta
                venta.iva = ventaMomentanea.iva
                venta.precioBrutoTotal = ventaMomentanea.precioBrutoTotal
                venta.medioDePago = ventaMomentanea.medioDePago
                venta.usuario = ventaMomentanea.usuario
                venta.save()

            for ventaDetalleMomentanea in ventasDetalleMomentaneas:
                venta = Venta.objects.filter(numeroVenta = ventaDetalleMomentanea.numeroVenta.numeroVenta).first() #se pone first() para que sea una instancia y no un QuerySet
                prenda = Prenda.objects.filter(numeroPrenda = ventaDetalleMomentanea.numeroPrenda.numeroPrenda).first()

                ventaDetalle = VentaDetalle()
                ventaDetalle.numeroVenta = venta
                ventaDetalle.numeroPrenda = prenda
                ventaDetalle.cantidadVendida = ventaDetalleMomentanea.cantidadVendida
                ventaDetalle.precioNetoUnitario = ventaDetalleMomentanea.precioNetoUnitario
                ventaDetalle.precioNetoTotal = ventaDetalleMomentanea.precioNetoTotal
                ventaDetalle.save()

                cantidadDespuesDeVenta = prenda.cantidad - ventaDetalle.cantidadVendida

                prenda.cantidad = cantidadDespuesDeVenta
                prenda.save()

            VentaMomentanea.objects.filter(usuario = request.user).delete() #tambien se borran los detalles de venta momentaneos
            llave = 'numeroVentaEnCache' #Al registrar la orden de venta, se elimina del cache el numero de la venta en curso
            cache.delete(llave)
                            
            messages.success(request, "Orden de venta registrada")
            return redirect("ventas:index")
    else:
        formVenta = VentaForm()
        formVentaDetalle = VentaDetalleForm()     

    context = {"formVenta" : formVenta, "formVentaDetalle": formVentaDetalle, "ventas" : ventasMomentaneas, "ventasDetalle": ventasDetalleMomentaneas, "ventaEnCurso": True} #en context va la informacion que se envia a 'ventas/formulario.html'
    return render(request, 'ventas/formulario.html', context)

@user_passes_test(lambda usuario: not usuario.is_superuser)
@login_required
def obtenerPrecioPrenda(request, numeroPrenda):
    prenda = get_object_or_404(Prenda, numeroPrenda=numeroPrenda)
    data = {'precioNetoUnitario': prenda.precioNetoUnitario}
    return JsonResponse(data)