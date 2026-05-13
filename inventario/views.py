from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Inventario
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    #Equivalente a: SELECT codigoPrenda, nombrePrenda, descripcionPrenda, SUM(cantidad) FROM inventario GROUP BY codigoPrenda, nombrePrenda, descripcionPrenda;
    inventario = Inventario.objects.values('codigoPrenda', 'nombrePrenda', 'descripcionPrenda').annotate(cantidadTotal=Sum('cantidad'))
    context = {"inventario": inventario}
    return render(request, "inventario/index.html", context)
