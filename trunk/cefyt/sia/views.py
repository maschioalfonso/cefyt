from django.shortcuts import render
from django.http import HttpResponseRedirect
from sia.models import Pais, Alumno
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from sia.forms import UsuarioForm, RegistroForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def index(request):

    context = {
               'mensaje': 'hola_mundo'}
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
@login_required
def cuenta(request):
    import ipdb; ipdb.set_trace()
    objects = User.objects.all()
    context = {'titulo': "Informacion de la cuenta",
               'object_list': objects
    }
    return render(request, 'sia/cuenta.html', context)

def registro(request):
    form = RegistroForm()

    if request.method == "GET":
        form = RegistroForm()

    elif request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():

            usuario,creado = User.objects.get_or_create(
                username=request.POST.get('email'),
                first_name=form.cleaned_data.get('nombre'),
                last_name=form.cleaned_data.get('apellido'),
                )
            #(object, created)
            if not creado:
                pass
                #exploted
            else:
                usuario.set_password(request.POST.get('password'))
                usuario.save()
                alumno = Alumno.objects.create(
                    usuario=usuario,
                    documento=form.cleaned_data.get('documento'),
                    pais=form.cleaned_data.get('pais'),
                    fecha_de_nacimiento=form.cleaned_data.get('fecha_de_nacimiento'),
                    provincia=form.cleaned_data.get('provincia'),
                    localidad=form.cleaned_data.get('localidad'),
                    domicilio=form.cleaned_data.get('domicilio'),
                    telefono=form.cleaned_data.get('telefono'),
                    telefono_alter=form.cleaned_data.get('telefono_alter')
                )
                usuario = authenticate(username=usuario.username, password=request.POST.get('password'))
                login(request, usuario)
                import ipdb; ipdb.set_trace()
                return redirect("sia:cuenta")


    context = {'form': form}

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