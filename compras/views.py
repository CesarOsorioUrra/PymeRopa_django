from django.shortcuts import render, redirect
from .models import Compra, CompraDetalle, CompraMomentanea, CompraDetalleMomentanea
from inventario.models import Prenda, PrendaMomentanea
from django.contrib.auth.decorators import login_required
from .forms import CompraForm, CompraDetalleForm, NumeroPrendaForm
from django.contrib import messages
from itertools import chain

# Create your views here.
@login_required
def index(request):
    if request.POST:
        action = request.POST.get("action") #para chequear en que botón se hizo click
        if action == 'Eliminar':
            Compra.objects.filter(usuario = request.user).delete()
            messages.success(request, "Sus compras han sido eliminadas")
            return redirect("compras:index")
        
    compras = Compra.objects.filter(usuario = request.user) #Para que el empleado pueda ver solo sus compras
    comprasDetalle = CompraDetalle.objects.filter(numeroCompra__usuario = request.user) #Para mostrar solo los detalles de compra de las compras realizadas por el empleado actual

    combined_list = list(chain(comprasDetalle))
    combined_list.sort(key=lambda obj: str(obj))

    context = {"compras" : compras, "data": combined_list}
    return render(request, "compras/index.html", context)

@login_required
def formulario(request):
    comprasMomentaneas = CompraMomentanea.objects.filter(usuario = request.user) #Para que el empleado pueda ver solo sus compras
    comprasDetalleMomentaneas = CompraDetalleMomentanea.objects.filter(numeroCompra__usuario = request.user) #Para mostrar solo los detalles de compra de las compras realizadas por el empleado actual

    combined_list = list(chain(comprasDetalleMomentaneas))
    combined_list.sort(key=lambda obj: str(obj))

    if request.POST:
        formCompra = CompraForm(request.POST)
        formCompraDetalle = CompraDetalleForm(request.POST)
        formNumeroPrenda = NumeroPrendaForm(request.POST) #se usa un form distinto para el numero de prenda para que pueda ingresarse una prenda que un no esté registrada y así no haya conflicto con la FK de CompraDetalle

        action = request.POST.get("action") #para chequear en que botón se hizo click

        if action == 'Agregar':
            if formCompra.is_valid() and formCompraDetalle.is_valid() and formNumeroPrenda.is_valid():
                compraMomentanea = CompraMomentanea()
                compraDetalleMomentanea = CompraDetalleMomentanea()

                numeroCompra = formCompra.cleaned_data.get("numeroCompra")

                compraMomentanea.numeroCompra = numeroCompra
                compraMomentanea.fechaCompra = formCompra.cleaned_data.get("fechaCompra")
                compraMomentanea.iva = formCompra.cleaned_data.get("iva")
                compraMomentanea.precioBrutoTotal = formCompra.cleaned_data.get("precioBrutoTotal")
                compraMomentanea.medioDePago = formCompra.cleaned_data.get("medioDePago")
                compraMomentanea.nombreProveedor = formCompra.cleaned_data.get("nombreProveedor")
                compraMomentanea.direccionProveedor = formCompra.cleaned_data.get("direccionProveedor")
                compraMomentanea.usuario = request.user
                compraMomentanea.save()

                #Como el detalle de compra tiene como FK el numero de Prenda, antes de crear la orden de compra, debe añadirse  en base de datos la Prenda con ese numero
                #Se debe verificar si la Prenda esta registrada, si lo está entonces se obtiene su cantidad
                #Esto es para la compra momentanea (para la orden de compra antes de registrarla)

                numeroPrenda = formNumeroPrenda.cleaned_data.get("numeroPrenda")
                cantidadComprada = formCompraDetalle.cleaned_data.get("cantidadComprada")

                #Se verifica si la prenda esta o no registrada en base de datos mediante el metodo .exists()
                prendaEstaRegistrada = Prenda.objects.filter(numeroPrenda = numeroPrenda).exists()              

                cantidadPrendaRegistrada = 0

                #Los atributos de la prenda momentanea se copiaran a los de la prenda definitiva solo si se acepta la orden de compra
                if prendaEstaRegistrada:
                    #Se obtiene la cantidad de la prenda registrada y luego se le asigna esa cantidad a la prenda momentanea
                    prenda = Prenda.objects.get(numeroPrenda = numeroPrenda)
                    cantidadPrendaRegistrada = prenda.cantidad                

                prendaMomentanea = PrendaMomentanea()
                prendaMomentanea.numeroPrenda = numeroPrenda
                prendaMomentanea.nombrePrenda = formCompraDetalle.cleaned_data.get("nombrePrenda")
                prendaMomentanea.descripcionPrenda = formCompraDetalle.cleaned_data.get("descripcionPrenda")
                prendaMomentanea.cantidad = cantidadPrendaRegistrada + cantidadComprada
                prendaMomentanea.precioNetoUnitario = formCompraDetalle.cleaned_data.get("precioNetoUnitario")
                prendaMomentanea.usuario = request.user
                prendaMomentanea.save()

                compraDetalleMomentanea.numeroCompra = compraMomentanea #se pone una instancia de CompraMomentanea pq la FK numeroCompra referencia a tabla CompraMomentanea
                compraDetalleMomentanea.numeroPrenda = prendaMomentanea #se pone una instancia de PrendaMomentanea pq la FK numeroPrenda referencia a tabla PrendaMomentanea
                compraDetalleMomentanea.nombrePrenda = formCompraDetalle.cleaned_data.get("nombrePrenda")
                compraDetalleMomentanea.descripcionPrenda = formCompraDetalle.cleaned_data.get("descripcionPrenda")
                compraDetalleMomentanea.cantidadComprada = cantidadComprada
                compraDetalleMomentanea.precioNetoUnitario = formCompraDetalle.cleaned_data.get("precioNetoUnitario")
                compraDetalleMomentanea.precioNetoTotal = formCompraDetalle.cleaned_data.get("precioNetoTotal")
                compraDetalleMomentanea.save()
                
                messages.success(request, "Compra agregada a orden de compra")
                return redirect("compras:formulario")
            
        elif action == 'Eliminar':
            CompraMomentanea.objects.filter(usuario = request.user).delete()
            PrendaMomentanea.objects.filter(usuario = request.user).delete()
            messages.success(request, "Su orden de compra ha sido eliminada")
            return redirect("compras:formulario") 

        #El boton para registrar ignora validaciones de los inputs del formulario en el cliente y en el servidor
        elif action == 'Registrar':
            for compraMomentanea in comprasMomentaneas:
                compra = Compra()
                compra.numeroCompra = compraMomentanea.numeroCompra
                compra.fechaCompra = compraMomentanea.fechaCompra
                compra.iva = compraMomentanea.iva
                compra.precioBrutoTotal = compraMomentanea.precioBrutoTotal
                compra.medioDePago = compraMomentanea.medioDePago
                compra.nombreProveedor = compraMomentanea.nombreProveedor
                compra.direccionProveedor = compraMomentanea.direccionProveedor
                compra.usuario = compraMomentanea.usuario
                compra.save()
            
            #prendas que ha momentaneamente registrado el usuario actual
            prendasMomentaneas = PrendaMomentanea.objects.filter(usuario = request.user)
            for prendaMomentanea in prendasMomentaneas:
                prendaEstaRegistrada = Prenda.objects.filter(numeroPrenda = prendaMomentanea.numeroPrenda).exists()
                if prendaEstaRegistrada:
                    prenda = Prenda.objects.get(numeroPrenda = prendaMomentanea.numeroPrenda)
                    prenda.nombrePrenda = prendaMomentanea.nombrePrenda
                    prenda.descripcionPrenda = prendaMomentanea.descripcionPrenda
                    prenda.cantidad = prendaMomentanea.cantidad
                    prenda.precioNetoUnitario = prendaMomentanea.precioNetoUnitario
                    prenda.save()
                else:
                    prenda = Prenda()
                    prenda.numeroPrenda = prendaMomentanea.numeroPrenda
                    prenda.nombrePrenda = prendaMomentanea.nombrePrenda
                    prenda.descripcionPrenda = prendaMomentanea.descripcionPrenda
                    prenda.cantidad = prendaMomentanea.cantidad
                    prenda.precioNetoUnitario = prendaMomentanea.precioNetoUnitario
                    prenda.save()

            for compraDetalleMomentanea in comprasDetalleMomentaneas:
                #compraDetalleMomentanea.numeroCompra.numeroCompra se pone numeroCompra dos veces pq primero se selecciona el atributo que es solo una FK (una referencia a la tabla Compra),
                #y luego se pone el otro numeroCompra que ya es el valor de numeroCompra que pertenece a la tabla Compra
                #lo mismo para prenda
                #siempre que se quiere buscar el valor de una FK se debe poner dos veces el atributo, primero el nombre del atributo en la tabla que está referenciando a otra, y luego el nombre del atributo que esta en la tabla que fué referenciada
                compra = Compra.objects.filter(numeroCompra = compraDetalleMomentanea.numeroCompra.numeroCompra).first() #se pone first() para que sea una instancia y no un QuerySet
                prenda = Prenda.objects.filter(numeroPrenda = compraDetalleMomentanea.numeroPrenda.numeroPrenda).first()

                compraDetalle = CompraDetalle()
                compraDetalle.numeroCompra = compra #a una FK se le debe asignar la tabla a la que referencia, no un valor para ese atributo
                compraDetalle.numeroPrenda = prenda #a una FK se le debe asignar la tabla a la que referencia, no un valor para ese atributo
                compraDetalle.descripcionPrenda = compraDetalleMomentanea.descripcionPrenda
                compraDetalle.cantidadComprada = compraDetalleMomentanea.cantidadComprada
                compraDetalle.precioNetoUnitario = compraDetalleMomentanea.precioNetoUnitario
                compraDetalle.precioNetoTotal = compraDetalleMomentanea.precioNetoTotal
                compraDetalle.save()

            CompraMomentanea.objects.filter(usuario = request.user).delete() #tambien se borran los detalles de compras momentaneas
            PrendaMomentanea.objects.filter(usuario = request.user).delete()

            messages.success(request, "Orden de compra registrada")
            return redirect("compras:index")
    else:
        formCompra = CompraForm()
        formCompraDetalle = CompraDetalleForm()   
        formNumeroPrenda = NumeroPrendaForm()

    context = {"formCompra" : formCompra, "formCompraDetalle": formCompraDetalle, "formNumeroPrenda": formNumeroPrenda, "compras" : comprasMomentaneas, "data": combined_list} #en context va la informacion que se envia a 'compras/formulario.html'
    return render(request, 'compras/formulario.html', context)