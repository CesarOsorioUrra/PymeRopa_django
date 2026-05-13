from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Compra
from django.contrib.auth.decorators import login_required
from .forms import ComprasForm
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
    compras = Compra.objects.order_by("-id")
    context = {"compras" : compras}
    return render(request, "compras/index.html", context)

@login_required
def formulario(request):
    ordenDeCompra = []
    if request.POST:
        form = ComprasForm(request.POST)
        """
        se tiene dos botones en el formulario, uno para agregar una compra a la orden de compra, y otro para que todas las compras
        en la orden de compra se guarden en la base de datos
        entonces, se puede diferenciar estos dos botones por su atributo 'name'. El boton para agregar una compra a la orden de
        compra se llama 'agregar', mientras que el boton para registrar todas las compras de la orden de compra actual se llama 'registrar'
        """
        if 'agregar' in request == 'POST':
            if form.is_valid():
                compra = Compra()

                compra.numeroCompra = form.cleaned_data.get("numeroCompra")
                compra.fechaCompra = form.cleaned_data.get("fechaCompra")
                compra.codigoPrenda = form.cleaned_data.get("codigoPrenda")
                compra.nombrePrenda = form.cleaned_data.get("nombrePrenda")
                compra.descripcionPrenda = form.cleaned_data.get("descripcionPrenda")
                compra.cantidadComprada = form.cleaned_data.get("cantidadComprada")
                compra.precioNetoUnitario = form.cleaned_data.get("precioNetoUnitario")
                compra.precioNetoTotal = form.cleaned_data.get("precioNetoTotal")
                compra.iva = form.cleaned_data.get("iva")
                compra.precioBrutoTotal = form.cleaned_data.get("precioBrutoTotal")
                compra.medioDePago = form.cleaned_data.get("medioDePago")
                compra.nombreProveedor = form.cleaned_data.get("nombreProveedor")
                compra.direccionProveedor = form.cleaned_data.get("direccionProveedor")

                ordenDeCompra.append(compra)
                messages.success(request, "Compra agregada a orden de compra")
                
        elif 'registrar' in request == 'POST':
            for compra in ordenDeCompra:
                compra.save()

            messages.success(request, "Compras de orden de compra registradas")
            return redirect("compras:index")
    else:
        form = ComprasForm()     

    context = {"form" : form, "compras" : ordenDeCompra} #en context va la informacion que se envia a 'compras/formulario.html'
    return render(request, 'compras/formulario.html', context)