# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet


from sia.models import Pais, Alumno, Cursado, DescubrimientoOpcion, DescubrimientoCurso, Cuota
from sia.forms import RegistroForm

import time


@login_required
def cuenta(request):
    if request.method == "GET" and request.user.is_superuser:
        return redirect("admin:index")

    usuario = User.objects.get(username=request.user.username)
    alumno = Alumno.objects.get(usuario=usuario)

    cursados = Cursado.objects.filter(inscripcion_abierta=True).exclude(alumno=alumno)
    cursados_inscripto = Cursado.objects.filter(alumno=alumno)
    lista_cuotas = Cuota.objects.filter(alumno=alumno, pagado=True)

    opciones_descubrimiento = DescubrimientoOpcion.objects.all()

    if request.method == "POST":
        if cursados:

            # Inscripci0n
            cursado = Cursado.objects.get(id=request.POST.get('curso'))
            cursado.alumno.add(alumno)
            cursado.save()

            # Generacion de cuotas
            cantidad_cuotas = cursado.duracion
            for i in range(1, cantidad_cuotas + 1):
                cuota = Cuota(alumno=alumno,
                              cursado=cursado,
                              numero=i,
                              costo_certificado_dolares = 0,
                              costo_certificado_pesos = 0,
                              valor_cuota_pesos = cursado.valor_cuota_pesos,
                              valor_cuota_dolares = cursado.valor_cuota_dolares
                        )
                cuota.save()

            # Costo certificado
            cuota_certificado = Cuota(alumno=alumno,
                                    cursado=cursado,
                                    numero=cantidad_cuotas + 1,
                                    costo_certificado_dolares = cursado.costo_certificado_dolares,
                                    costo_certificado_pesos = cursado.costo_certificado_pesos,
                                    valor_cuota_pesos = 0,
                                    valor_cuota_dolares = 0
                                )
            cuota_certificado.save()

        if opciones_descubrimiento:
            opcion = DescubrimientoOpcion.objects.get(id=request.POST.get('descubrimiento'))
            descubrimiento_curso = DescubrimientoCurso(cursada=cursado, alumno=alumno, opcion=opcion)
            descubrimiento_curso.save()

        return redirect("sia:cuenta")

    context = {'titulo': "Informacion de la cuenta de: ",
               'lista_cursados': cursados,
               'lista_cursados_inscripto' : cursados_inscripto,
               'opcion_descubrimiento' : opciones_descubrimiento,
               'lista_cuotas' : lista_cuotas
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

    if request.method == 'POST':
        cursado = Cursado.objects.get(id=request.POST.get('curso'))
        return generar_pdf(cursado)

    context = {'lista_cursados': cursados}
    return render(request, 'sia/generar_reporte.html', context)


def generar_pdf(cursado):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="somefilename.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # Titulo pagina
    titulo = Paragraph("CEFyT - Centro de Estudios Filosóficos y Teológicos", styles["Heading2"])
    elements.append(titulo)

    # Cursado
    curso = Paragraph("Curso: " + str(cursado), styles["Normal"])
    elements.append(curso)

    # Fecha
    fecha = Paragraph("Fecha: " + time.strftime("%c"), styles["Normal"])
    elements.append(fecha)

    # Listado de inscriptos
    cantidad_inscriptos = 0
    alumnos = []
    alumnos.append(['Apellido', 'Nombre', 'Documento', 'País', 'Provincia', 'Localidad', 'Nombre de usuario'])
    for alumno in cursado.alumno.all():
        alumnos.append([alumno.usuario.last_name, alumno.usuario.first_name, alumno.documento, alumno.pais, alumno.provincia, alumno.localidad, alumno.usuario.username])
        cantidad_inscriptos = cantidad_inscriptos + 1

    numero_inscriptos = Paragraph("Cantidad de inscriptos: " + str(cantidad_inscriptos), styles["Normal"])
    elements.append(numero_inscriptos)

    linea_vacia = Paragraph(".", styles["Normal"])
    elements.append(linea_vacia)

    # Tabla de alumnos
    datos = alumnos
    t = Table(datos)
    t.setStyle(TableStyle([('BACKGROUND', (0,0),(6,0), colors.lavender),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
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
