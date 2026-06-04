from django.shortcuts import render, redirect
from .models import Venta, VentaDetalle, VentaMomentanea, VentaDetalleMomentanea
from django.contrib.auth.decorators import login_required
from .forms import VentaForm, VentaDetalleForm
from django.contrib import messages
from inventario.models import Prenda
from itertools import chain

# Create your views here.
@login_required
def index(request):
    if request.POST:
        action = request.POST.get("action") #para chequear en que botón se hizo click
        if action == 'Eliminar':
            Venta.objects.filter(usuario = request.user).delete()
            messages.success(request, "Sus ventas han sido eliminadas")
            return redirect("ventas:index")
        
    
    ventas = Venta.objects.filter(usuario = request.user) #Para que el empleado pueda ver solo sus ventas
    ventasDetalle = VentaDetalle.objects.filter(numeroVenta__usuario = request.user) #Para mostrar solo los detalles de venta de las ventas realizadas por el empleado actual

    combined_list = list(chain(ventasDetalle))
    combined_list.sort(key=lambda obj: str(obj))

    context = {"ventas" : ventas, "data": combined_list}
    return render(request, "ventas/index.html", context)

@login_required
def formulario(request):
    ventasMomentaneas = VentaMomentanea.objects.filter(usuario = request.user)
    ventasDetalleMomentaneas = VentaDetalleMomentanea.objects.filter(numeroVenta__usuario = request.user)

    combined_list = list(chain(ventasDetalleMomentaneas))
    combined_list.sort(key=lambda obj: str(obj))

    if request.POST:
        formVenta = VentaForm(request.POST)
        formVentaDetalle = VentaDetalleForm(request.POST)
        
        action = request.POST.get("action") #para chequear en que botón se hizo click
        
        if action == 'Agregar':
            if formVenta.is_valid() and formVentaDetalle.is_valid():

                numeroPrenda = formVentaDetalle.cleaned_data.get("numeroPrenda").numeroPrenda
                cantidadVendida = formVentaDetalle.cleaned_data.get("cantidadVendida")
                cantidadPrenda = Prenda.objects.get(numeroPrenda = numeroPrenda).cantidad
                
                if cantidadVendida > cantidadPrenda:
                    messages.error(request, f"""No puede vender mayor cantidad de prendas de las que se tiene. En
                                     el inventario se tiene {cantidadPrenda} unidades, pero usted puso {cantidadVendida} unidades.""")
                    return redirect("ventas:formulario")

                ventaMomentanea = VentaMomentanea()
                ventaDetalleMomentanea = VentaDetalleMomentanea()

                ventaMomentanea.numeroVenta = formVenta.cleaned_data.get("numeroVenta")
                ventaMomentanea.fechaVenta = formVenta.cleaned_data.get("fechaVenta")
                ventaMomentanea.iva = formVenta.cleaned_data.get("iva")
                ventaMomentanea.precioBrutoTotal = formVenta.cleaned_data.get("precioBrutoTotal")
                ventaMomentanea.medioDePago = formVenta.cleaned_data.get("medioDePago")
                ventaMomentanea.usuario = request.user

                ventaMomentanea.save()

                ventaDetalleMomentanea.numeroVenta = ventaMomentanea
                ventaDetalleMomentanea.numeroPrenda = formVentaDetalle.cleaned_data.get("numeroPrenda")
                ventaDetalleMomentanea.cantidadVendida = formVentaDetalle.cleaned_data.get("cantidadVendida")
                ventaDetalleMomentanea.precioNetoUnitario = formVentaDetalle.cleaned_data.get("precioNetoUnitario")
                ventaDetalleMomentanea.precioNetoTotal = formVentaDetalle.cleaned_data.get("precioNetoTotal")

                ventaDetalleMomentanea.save()

                messages.success(request, "Venta agregada a orden de venta")
                return redirect("ventas:formulario")
            
        elif action == 'Eliminar':
            VentaMomentanea.objects.filter(usuario = request.user).delete()
            messages.success(request, "Su orden de venta ha sido eliminada")
            return redirect("ventas:formulario") 
        
        #El boton para registrar ignora validaciones de los inputs del formulario en el cliente y en el servidor
        elif action == 'Registrar':
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
                
            messages.success(request, "Orden de venta registrada")
            return redirect("ventas:index")
    else:
        formVenta = VentaForm()
        formVentaDetalle = VentaDetalleForm()     

    context = {"formVenta" : formVenta, "formVentaDetalle": formVentaDetalle, "ventas" : ventasMomentaneas, "data": combined_list} #en context va la informacion que se envia a 'ventas/formulario.html'
    return render(request, 'ventas/formulario.html', context)