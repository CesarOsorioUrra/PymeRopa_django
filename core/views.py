from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AvisoForm
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

@login_required
def aviso(request):
    if request.POST:
        aviso = AvisoForm(request.POST)
        if aviso.is_valid():
            #falta colocar logica para que aviso se publique en pagina de inicio de otros usuarios
            messages.success(request, "Aviso publicado correctamente")
            return redirect("aviso")
    else:
        aviso = AvisoForm()
    context = {"aviso" : aviso}
    return render(request, 'core/aviso.html', context)