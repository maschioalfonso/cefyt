from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from sia.models import Pais, Alumno, Cursado, DescubrimientoOpcion, DescubrimientoCurso
from sia.forms import RegistroForm


@login_required
def index(request):

    context = {'mensaje': 'hola_mundo'
              }
    return render(request, 'sia/cuenta.html', context)


@login_required
def cuenta(request):
    cursados = Cursado.objects.all()
    opcion_descubrimento = DescubrimientoOpcion.objects.all()
    context = {'titulo': "Informacion de la cuenta",
               'lista_cursados': cursados,
               'opcion_descubrimento' : opcion_descubrimento
              }

    if request.method == "POST" and not Cursado.objects.filter(inscripcion_abierta=True):
        cursado = Cursado.objects.get(id=request.POST.get('curso'))
        usuario = User.objects.get(username=request.user.username)
        #alumno = Alumno.objects.get(usuario_username='marianitovlk@gmail.com')
        cursado.alumno.add(alumno)
        

        opcion = DescubrimientoOpcion.objects.get(id=request.POST.get('descubrimiento'))
        descubrimiento_curso = DescubrimientoCurso(cursada=cursado, 
                                                   alumno=alumno, 
                                                   opcion=opcion)
        descubrimiento_curso.save()

    return render(request, 'sia/cuenta.html', context)


def registro(request):
    form = RegistroForm()

    usuario_existente = False
    if request.method == "GET":
        form = RegistroForm()

    elif request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():

            usuario,creado = User.objects.get_or_create(
                username=request.POST.get('email'),
                first_name=form.cleaned_data.get('nombre'),
                last_name=form.cleaned_data.get('apellido'),
                is_staff=True,
                )
            if not creado:
                usuario_existente = True
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
                #import ipdb; ipdb.set_trace()
                return redirect("sia:cuenta")


    context = {'form': form,
               'usuario_existente' : usuario_existente,
              }

    return render(request, 'sia/registro.html', context)
