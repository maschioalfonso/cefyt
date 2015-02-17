from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from sia.models import Pais, Alumno, Cursado, DescubrimientoOpcion, DescubrimientoCurso, Cuota
from sia.forms import RegistroForm



@login_required
def cuenta(request):
    if request.method == "GET" and request.user.is_superuser:
        return redirect("admin:index")

    usuario = User.objects.get(username=request.user.username)
    alumno = Alumno.objects.get(usuario=usuario)

    cursados = Cursado.objects.filter(inscripcion_abierta=True)
    cursados_inscripto = Cursado.objects.filter(alumno=alumno)

    opciones_descubrimiento = DescubrimientoOpcion.objects.all()

    if request.method == "POST":
        if cursados:

            # Inscripción
            cursado = Cursado.objects.get(id=request.POST.get('curso'))
            cursado.alumno.add(alumno)
            cursado.save()

            # Generación de cuotas
            cantidad_cuotas = cursado.duracion
            for i in range(1, cantidad_cuotas + 1):
                cuota = Cuota(alumno=alumno,
                              cursado=cursado,
                              numero=i,
                        )
                cuota.save()

        if opciones_descubrimiento:
            opcion = DescubrimientoOpcion.objects.get(id=request.POST.get('descubrimiento'))
            descubrimiento_curso = DescubrimientoCurso(cursada=cursado, alumno=alumno, opcion=opcion)
            descubrimiento_curso.save()

    context = {'titulo': "Informacion de la cuenta de: ",
               'lista_cursados': cursados,
               'lista_cursados_inscripto' : cursados_inscripto,
               'opcion_descubrimiento' : opciones_descubrimiento,
              }
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

def generar_reporte(request):
    cursados = Cursado.objects.filter()

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        cursado = Cursado.objects.get(id=request.POST.get('curso'))
        return generar_pdf(cursado)

    context = {'lista_cursados': cursados}
    return render(request, 'sia/generar_reporte.html', context)

def generar_pdf(cursado):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="somefilename.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    alumnos = []
    for alumno in cursado.alumno.all():
        alumnos.append([alumno.usuario.first_name, alumno.documento])


    datos = alumnos
    t = Table(datos)
    t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                          ]))
    elements.append(t)

    # write the document to disk
    doc.build(elements)

    return response

def reporte(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="somefilename.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    cursado = Cursado.objects.get(id=1)

    alumnos = []
    for alumno in cursado.alumno.all():
        alumnos.append([alumno.usuario.first_name, alumno.documento])


    datos = alumnos
    t = Table(datos)
    t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                          ]))
    elements.append(t)

    # write the document to disk
    doc.build(elements)

    return response