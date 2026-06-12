from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Prenda
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    prendas = Prenda.objects.all()
    context = {"prendas": prendas}
    return render(request, "inventario/index.html", context)
