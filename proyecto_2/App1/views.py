from django.shortcuts import render
from App1.forms import *
from App1.models import Cliente, Sucursal, Producto
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def inicio(request):
    clientes = Cliente.objects.all()
    suc = Sucursal.objects.all()
    prod = Producto.objects.all()
    return render(request, "App1/base.html", {"clientes": clientes, "sucursales": suc, "productos": prod})

@login_required
def productosFormulario(request):
    
    if request.method == 'POST':
 
            miFormulario = ProductoFormulario(request.POST ) 
            print(miFormulario)
 
            if miFormulario.is_valid():
                  informacion = miFormulario.cleaned_data
                  prod = Producto(nombre=informacion['nombre'], precio=informacion['precio'])
                  prod.save()
                  return inicio(request)
    else:
            miFormulario = ProductoFormulario()
 
    return render(request, "App1/ProductoFormulario.html", {"miFormulario": miFormulario})

@login_required
def sucursalesFormulario(request):
    
    if request.method == 'POST':
 
            miFormulario = SucursalFormulario(request.POST ) 
            print(miFormulario)
 
            if miFormulario.is_valid():
                  informacion = miFormulario.cleaned_data
                  suc = Sucursal(calle=informacion['calle'], altura=informacion['altura'])
                  suc.save()
                  return inicio(request)
    else:
            miFormulario = SucursalFormulario()
 
    return render(request, "App1/SucursalFormulario.html", {"miFormulario": miFormulario})
   
def clienteFormulario(request):
 
      if request.method == 'POST':
 
            miFormulario = ClienteFormulario(request.POST ) 
            print(miFormulario)
 
            if miFormulario.is_valid():
                  informacion = miFormulario.cleaned_data
                  cliente = Cliente(nombre=informacion['nombre'], email=informacion['email'],   edad=informacion['edad'])
                  cliente.save()
                  return inicio(request)
      else:
            miFormulario = ClienteFormulario()
 
      return render(request, "App1/clienteFormulario.html", {"miFormulario": miFormulario}) 

def buscarCli(request):
    
    if request.method == 'POST':
         
            miFormulario = BusquedaCliente(request.POST ) 
            print(miFormulario)
 
            if miFormulario.is_valid():
                informacion = miFormulario.cleaned_data
                clientes = Cliente.objects.filter(nombre__icontains=informacion["nombre"])
                return render(request, "App1/listacli.html", {"clientes": clientes})
            else:
                print("\n\nERROR IS_VALID FALSE\n\n")
    else:
        miFormulario = BusquedaCliente()
 
    return render(request, "App1/clienteFormulario.html", {"miFormulario": miFormulario})

def borrarproducto(request, prod_id):
    
    try:
        producto = Producto.objects.get(id=int(prod_id))
        
        producto.delete()
        return inicio(request)
    except:
        return inicio(request)

class ClienteListView(ListView):
    model=Cliente
    template_name= "App1/listacli.html"
    
class ProdDetalleView(LoginRequiredMixin, DetailView):
    model=Producto
    template_name= "App1/Prod_detalle.html"
    
class  ClienteCreateView(LoginRequiredMixin, CreateView):
    model=Cliente
    template_name= "App1/clienteFormulario.html"
    success_url = reverse_lazy("List")
    fields=["nombre", "email", "edad"]
    
class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model=Cliente
    template_name= "App1/clienteEd.html"
    success_url = reverse_lazy("List")
    fields = ["nombre", "email", "edad"]

class ProdDeleteView(LoginRequiredMixin, DeleteView):
    model=Producto
    success_url = reverse_lazy("BorrarProd")
    template_name= "App1/base.html"
    
#vista de login
def login_request(request):
    msg_login = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username= usuario, password=contrasenia)

            if user is not None:
                login(request, user)
                return inicio(request)

        msg_login = "Usuario o contraseña incorrectos"

    form = AuthenticationForm()
    return render(request, "App1/login.html", {"form": form, "msg_login": msg_login})

# Vista de registro
def register(request):

      if request.method == 'POST':

            #form = UserCreationForm(request.POST)
            form = UserRegisterForm(request.POST)
            if form.is_valid():

                  username = form.cleaned_data['username']
                  form.save()
                  return render(request,"App1/registro.html" ,  {"mensaje":"Usuario Creado :)"})

      else:
            #form = UserCreationForm()       
            form = UserRegisterForm()     

      return render(request,"App1/registro.html" ,  {"form":form})

