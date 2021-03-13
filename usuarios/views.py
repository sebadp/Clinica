from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, "clinica/base.html")

# def index(request):
#     return render(request, "usuarios/index.html")

def index(request):
# Si ningún usuario ha iniciado sesión, vuelva a la página de inicio de sesión :
    if not request.user.is_authenticated:
        # return HttpResponseRedirect(reverse("usuarios:login"))
        return HttpResponseRedirect(reverse("clinica:index"))
    # return render(request, "clinica/base.html")
    return HttpResponseRedirect(reverse("clinica:index"))

def login_view(request):
    if request.method == "POST":
        # Accediendo al nombre de usuario y contraseña desde los datos del formulario
        # nombreusuario
        username = request.POST["username"]
        password = request.POST["password"]
        #  Verifique si el nombre de usuario y la contraseña son correctos, devolviendo el objeto Usuario si es así
        user = authenticate(request, username=username, password=password)
        # Si se devuelve el objeto de usuario, inicie sesión y diríjase a la página de índice:        
        if user is not None:            
            # Hacemos el login manualmente
            login(request, user)
            # Y le redireccionamos al index
            return HttpResponseRedirect(reverse("clinica:index"))
        else:
            # De lo contrario, regrese la página de inicio de sesión nuevamente con un nuevo contexto            
            return render(request, "usuarios/login.html", {
                "mensaje": "Credenciales no validas."
            })
    else:
        return render(request, "usuarios/login.html")
        # return HttpResponseRedirect(reverse("clinica:index"))

def logout_view(request):
    logout(request)
    # return render(request, "usuarios/login.html", {"mensaje": "Desconectado."})
    return HttpResponseRedirect(reverse("clinica:index"))