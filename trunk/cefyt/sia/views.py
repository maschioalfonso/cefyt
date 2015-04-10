# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.views import logout

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from reportlab.graphics.barcode.common import I2of5
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import *


from sia.models import Pais, Alumno, Cursado, DescubrimientoOpcion, DescubrimientoCurso, Cuota
from sia.forms import RegistroForm

import time


@login_required
def cuenta(request):
    if request.method == "GET" and request.user.is_superuser:
        return redirect("admin:index")

    usuario = User.objects.get(username=request.user.username)
    alumno = Alumno.objects.get(usuario=usuario)

    es_Argentino = alumno.pais.nombre == "Argentina"

    cursados = Cursado.objects.filter(inscripcion_abierta=True).exclude(alumno=alumno)
    cursados_inscripto = Cursado.objects.filter(alumno=alumno)
    lista_cuotas = Cuota.objects.filter(alumno=alumno)

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
                cuota = Cuota(
                    alumno=alumno,
                    cursado=cursado,
                    numero=i,
                    costo_certificado_dolares=0,
                    costo_certificado_pesos=0,
                    valor_cuota_pesos=cursado.valor_cuota_pesos,
                    valor_cuota_dolares=cursado.valor_cuota_dolares)
                cuota.save()

            # Costo certificado
            cuota_certificado = Cuota(
              alumno=alumno,
              cursado=cursado,
              numero=cantidad_cuotas + 1,
              costo_certificado_dolares=cursado.costo_certificado_dolares,
              costo_certificado_pesos=cursado.costo_certificado_pesos,
              valor_cuota_pesos=0,
              valor_cuota_dolares=0)
            cuota_certificado.save()

        if opciones_descubrimiento:
            opcion = DescubrimientoOpcion.objects.get(id=request.POST.get('descubrimiento'))
            descubrimiento_curso = DescubrimientoCurso(cursada=cursado, alumno=alumno, opcion=opcion)
            descubrimiento_curso.save()

        return redirect("sia:cuenta")

    context = {'lista_cursados': cursados,
               'es_Argentino': es_Argentino,
               'lista_cursados_inscripto': cursados_inscripto,
               'opcion_descubrimiento': opciones_descubrimiento,
               'lista_cuotas': lista_cuotas}
    return render(request, 'sia/cuenta.html', context)


def registro(request):
    form = RegistroForm()

    usuario_existente = False
    if request.method == "GET":
        form = RegistroForm()

    elif request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():

            usuario, creado = User.objects.get_or_create(
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
                # import ipdb; ipdb.set_trace()
                return redirect("sia:cuenta")

    context = {'form': form,
               'usuario_existente': usuario_existente}

    return render(request, 'sia/registro.html', context)


@login_required
def listado_cuotas(request):
    context = {}
    return render(request, 'sia/listado_cuotas.html', context)


def generar_reporte(request):
    if not request.user.is_superuser:
        return redirect("sia:cuenta")

    cursados = Cursado.objects.filter()

    if request.method == 'POST':
        cursado = Cursado.objects.get(id=request.POST.get('curso'))
        return generar_pdf(cursado)

    context = {'lista_cursados': cursados}
    return render(request, 'sia/generar_reporte.html', context)


def generar_pdf(cursado):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="%s".pdf' % (cursado.nombre)

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # Titulo página
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

    if cantidad_inscriptos > 0:
        # Tabla de alumnos
        t = Table(alumnos)
        t.setStyle(TableStyle(
            [('BACKGROUND', (0, 0), (6, 0), colors.lavender),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        elements.append(t)

    doc.build(elements)

    return response


def generar_cupon(request):
    response = HttpResponse(content_type='application/pdf')

    usuario = User.objects.get(username=request.user.username)
    alumno = Alumno.objects.get(usuario=usuario)
    cuota = Cuota.objects.get(id=request.POST.get('cuota'))

    cupon_valor = str('%.2f' % cuota.valor_cuota_pesos)


    # Generación del número cupón
    nro_gire = "4057"           # Valor fijo
    nro_cliente = "00001"       # Número de cliente: 5 dígitos
    tipo_comprobante = "1"      # Tipo de comprobante: 1 dígito
    nro_comprobante = "000001"  # Número de comprobante: 6 dígitos
    importe = cupon_valor.replace(".", "") # Importe: 4 parte entera, 2 parte decimal
    anio_vencimiento = "15"     # Año vencimiento: 2 dígitos
    mes_vencimiento = "05"      # Mes vencimiento: 2 dígitos
    dia_vencimiento = "31"      # Día vencimiento: 2 dígitos
    reservado = "0"             # Espacio reservado
    digito_verificador = "9"    # Digito verificador

    nro_cupon = nro_gire + nro_cliente + tipo_comprobante +\
                nro_comprobante + importe + anio_vencimiento +\
                mes_vencimiento + dia_vencimiento + reservado +\
                digito_verificador

    # Nombre del archivo
    cupon = "Cupon"
    response['Content-Disposition'] = 'filename="%s".pdf' %(cupon)

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Imagen
    logo = Image('./sia/static/sia/cupon/logo.png')
    logo.drawHeight = 1.40*25.4*mm*logo.drawHeight / logo.drawWidth
    logo.drawWidth = 1.40*25.4*mm

    # Datos del cupón
    titulo1 = Paragraph("SEMINARIO VILLA CLARET", styles["Heading2"])
    titulo2 = Paragraph("CEFyT - Centro de Estudios Filosóficos y Teológicos", styles["Heading5"])

    apellido = alumno.usuario.last_name
    nombre = alumno.usuario.first_name

    domicilio = alumno.domicilio
    localidad = alumno.localidad
    provincia = alumno.provincia
    pais = alumno.pais.nombre

    nro_cuota = "Cuota numero " + str(cuota.numero)
    cursado = "Curso " + cuota.cursado.nombre
    valor_cuota = "$" + cupon_valor

    # Código barras
    tb=0.254320987654 * mm # thin bar
    bh=20 * mm # bar height
    bc=I2of5(
      nro_cupon, barWidth=tb, ratio=3, barHeight=bh, bearers=0, 
      quiet=0, checksum=1)

    datos = [[logo, titulo1],
             ['', titulo2],
             ['', "Av. Padre Claret 5601"],
             ['', "Bº Padre Claret"],
             ['', "X5022LJQ Córdoba, República Argentina"],
             ['', "C.U.I.T.: 30-67870110-2"],
             [],
             ['Señor/a:', apellido + ', ' + nombre],
             ['Domicilio:', domicilio + ', ' + localidad + ', ' + provincia + ', ' + pais],
             ['En concepto de:', nro_cuota + ', ' + cursado],
             ['Total a pagar:', valor_cuota],
             [],
             [bc],
             [nro_cupon]
            ]

    t = Table(datos)
    t.setStyle(TableStyle([# Logo
                           ('SPAN', (0, 0), (0, -9)),
                           ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                           ('VALIGN', (0, 0), (0, 0), 'CENTER'),

                           ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                           ('FONTNAME', (0, 2), (0, -4), 'Helvetica-Bold'),

                           # Código de barras
                           ('SPAN', (0, -2), (1, -2)),
                           ('ALIGN', (0, -2), (1, -2), 'CENTER'),

                           # Número de cupón
                           ('SPAN', (0, -1), (1, -1)),
                           ('ALIGN', (0, -1), (1, -1), 'CENTER'),

                           ('GRID', (0, 0), (-1, -1), 1, colors.gray),
                          ]))

    elements.append(t)
    doc.build(elements)

    return response

# BUG: Si se registra, intenta inscribirse a un curso y
# pone cancelar al cartel de advertencia.
