from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Venta
from django.contrib.auth.decorators import login_required
from .forms import VentasForm
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
    ventas = Venta.objects.filter(usuario=request.user).order_by("-id")
    context = {"ventas" : ventas}
    return render(request, "ventas/index.html", context)

@login_required
def formulario(request):
    ordenDeVenta = []
    if request.POST:
        form = VentasForm(request.POST)
        """
        se tiene dos botones en el formulario, uno para agregar una venta a la orden de venta, y otro para que todas las ventas
        en la orden de venta se guarden en la base de datos
        entonces, se puede diferenciar estos dos botones por su atributo 'name'. El boton para agregar una venta a la orden de
        venta se llama 'agregar', mientras que el boton para registrar todas las ventas de la orden de venta actual se llama 'registrar'
        """
        if 'agregar' in request == 'POST':
            if form.is_valid():
                venta = Venta()

                venta.numeroVenta = form.cleaned_data.get("numeroVenta")
                venta.fechaVenta = form.cleaned_data.get("fechaVenta")
                venta.codigoPrenda = form.cleaned_data.get("codigoPrenda")
                venta.nombrePrenda = form.cleaned_data.get("nombrePrenda")
                venta.descripcionPrenda = form.cleaned_data.get("descripcionPrenda")
                venta.cantidadVendida = form.cleaned_data.get("cantidadVendida")
                venta.precioNetoUnitario = form.cleaned_data.get("precioNetoUnitario")
                venta.precioNetoTotal = form.cleaned_data.get("precioNetoTotal")
                venta.iva = form.cleaned_data.get("iva")
                venta.precioBrutoTotal = form.cleaned_data.get("precioBrutoTotal")
                venta.medioDePago = form.cleaned_data.get("medioDePago")

                ordenDeVenta.append(venta)
                messages.success(request, "Venta agregada a orden de venta")
                
        elif 'registrar' in request == 'POST':
            for venta in ordenDeVenta:
                venta = form.save(commit=False)
                venta.usuario = request.user
                venta.save()
                
            messages.success(request, "Ventas de orden de venta registradas")
            return redirect("ventas:index")
    else:
        form = VentasForm()     

    context = {"form" : form, "ventas" : ordenDeVenta} #en context va la informacion que se envia a 'ventas/formulario.html'
    return render(request, 'ventas/formulario.html', context)