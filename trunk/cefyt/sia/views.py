from django.shortcuts import render
from django.http import HttpResponseRedirect
from sia.models import Pais, Alumno
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from sia.forms import UsuarioForm


#@login_required(redirect_field_name='my_redirect_field')
def index(request):
    context = {'form': UsuarioForm}
    return render(request, 'sia/index.html', context)



# def login(request):
#   form = myform

#   if request.method == 'GET':
#     pass

#   elif request.methon == 'POST':
#     if form.is_valid():
#       usuario = request.POST.get('usuario')
#       contrasenia = request.POST.get('password')
#       usuario = authenticate(usuario, contrasenia)
#       if usuario.is_authenticated:
#         redirect()
  

#   context = {'form' = form}
#   return render(request, 'mytemplate.html', context)






def cuenta(request):
    import ipdb; ipdb.set_trace()
    nombre_usuario = request.POST.get('username')
    contrasenia = request.POST.get('password')
    if (nombre_usuario == None) or (contrasenia == None):
        return HttpResponseRedirect('/sia')

    import ipdb; ipdb.set_trace()
    usuario = authenticate(username=nombre_usuario, password=contrasenia)
    if usuario.is_authenticated():
      autenticado = True
    else:
      autenticado = False
      return HttpResponseRedirect('/sia')


    context = {
      'autenticado' : autenticado,
      'usuario' : usuario,
    }
    return render(request, 'sia/cuenta.html', context)

def registro(request):
    paises = Pais.objects.all()
    context = {'paises' : paises}
    return render(request, 'sia/registro.html', context)

def cursos_dusponible(request):
    activos = Cursado.objects.all().filter(inscripcion_abierta = True)
  




def crear_registro(request):
    apellido = request.POST.get['apellido']
    nombres = request.POST['nombres']
    documento = request.POST['documento']
    fecha_de_nacimiento = request.POST['fecha_de_nacimiento']
    pais = request.POST['pais']
    provincia = request.POST['provincia']
    localidad = request.POST['localidad']
    domicilio = request.POST['domicilio']
    telefono = request.POST['telefono']
    telefono_alter = request.POST['telefono_alter']
    email = request.POST['email']
    pwd = request.POST['pwd']
    pais = Pais.objects.get(id=pais)

    if not Alumno.objects.filter(email="email"):
      #definir web de error
      return HttpResponseRedirect('/sia')
    else:
      nuevo_alumno = Alumno(apellido = apellido,
                          nombres = nombres,
                          documento = documento,
                          fecha_de_nacimiento = fecha_de_nacimiento,
                          pais = pais,
                          provincia = provincia,
                          localidad = localidad,
                          domicilio = domicilio,
                          telefono = telefono,
                          telefono_alter = telefono_alter,
                          email = email)

      
    

      nuevo_alumno.save()
      
      # TO DO:
      # Catchear excepciones
      user = User.objects.create_user(email, email, pwd)


      datos = apellido + nombres + documento + fecha_de_nacimiento + provincia + localidad + domicilio + telefono + telefono_alter + email + pwd
      


      # TO DO: Crear un nuevo usuario usando el sistema de usuario de Django:
      # Ver: https://docs.djangoproject.com/en/1.6/topics/auth/default/#user-objects

      # TO DO: Tener en cuenta, agregar relaciones ManyToMany
      # Cursado.objects.all()[0].alumno.add('diego@guzman.com')

      return HttpResponseRedirect('/sia')