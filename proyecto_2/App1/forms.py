from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ClienteFormulario(forms.Form):
    
    nombre = forms.CharField()
    edad = forms.IntegerField()
    email = forms.EmailField()
    
class ProductoFormulario(forms.Form):
    
    nombre = forms.CharField()
    precio = forms.FloatField()

class SucursalFormulario(forms.Form):   
     
    calle = forms.CharField()
    altura = forms.IntegerField()
    
    
class BusquedaCliente(forms.Form):
    
    nombre = forms.CharField()
    
    
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email valido")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
 
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # Saca los mensajes de ayuda
        help_texts = {k:"" for k in fields}
    