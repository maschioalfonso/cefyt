# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from reportlab.graphics.barcode.common import I2of5
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import *

from sia.models import (Alumno, Cursado, DescubrimientoOpcion,
                        DescubrimientoCurso, Cuota, Noticia)
from sia.forms import RegistroForm, SubirArchivoForm

from datetime import date

import time


NOMBRE_CEFYT = "CEFyT - Centro de Estudios Filosóficos y Teológicos"
DOMICILIO_CEFYT = "Av. Padre Claret 5601"
BARRIO_CEFYT = "Bº Padre Claret"
CUIT_CEFYT = "C.U.I.T.: 30-67870110-2"
CODPOSTAL_CEFYT = "X5022LJQ"
LOCALIDAD_CEFYT = "Córdoba"
PAIS_CEFYT = "Argentina"
NUMERO_GIRE = "4057"


def es_alumno(view):
    def control_alumno(request):
        usuario = User.objects.get(username=request.user.username)
        try:
            Alumno.objects.get(usuario=usuario)
        except Alumno.DoesNotExist:
            return redirect("/sia/")

        return view(request)

    return control_alumno


# @es_alumno
@login_required
def cuenta(request):
    if request.method == "GET" and request.user.is_superuser:
        return redirect("admin:index")

    alumno = obtener_alumno(request)
    alumno_es_argentino = es_argentino(alumno)
    noticias = Noticia.objects.all().order_by('-fecha')

    cursados = Cursado.objects.filter(
        inscripcion_abierta=True).exclude(alumno=alumno)
    cursados_inscripto = Cursado.objects.filter(alumno=alumno)

    opciones_descubrimiento = DescubrimientoOpcion.objects.all()

    if request.method == "POST":
        if cursados:

            cursado = Cursado.objects.get(id=request.POST.get('curso'))

            # Inscripción y generación de cuotas
            inscribir_alumno(alumno, cursado)
            generar_cuotas(alumno, cursado)

        if opciones_descubrimiento:
            opcion = DescubrimientoOpcion.objects.get(
                id=request.POST.get('descubrimiento'))

            DescubrimientoCurso.objects.create(
                cursada=cursado,
                alumno=alumno,
                opcion=opcion)

        return redirect("sia:cuenta")

    context = {'lista_cursados': cursados,
               'alumno_es_argentino': alumno_es_argentino,
               'lista_cursados_inscripto': cursados_inscripto,
               'opcion_descubrimiento': opciones_descubrimiento,
               'noticias': noticias
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
                Alumno.objects.create(
                    usuario=usuario,
                    documento=form.cleaned_data.get('documento'),
                    pais=form.cleaned_data.get('pais'),
                    fecha_de_nacimiento=form.cleaned_data.get(
                        'fecha_de_nacimiento'),
                    provincia=form.cleaned_data.get('provincia'),
                    localidad=form.cleaned_data.get('localidad'),
                    domicilio=form.cleaned_data.get('domicilio'),
                    telefono=form.cleaned_data.get('telefono'),
                    telefono_alter=form.cleaned_data.get('telefono_alter'))

                usuario = authenticate(
                    username=usuario.username,
                    password=request.POST.get('password'))
                login(request, usuario)

                return redirect("sia:cuenta")

    context = {'form': form,
               'usuario_existente': usuario_existente}

    return render(request, 'sia/registro.html', context)


@login_required
def listado_cuotas(request):

    alumno = obtener_alumno(request)
    alumno_es_argentino = es_argentino(alumno)
    lista_cuotas = Cuota.objects.filter(alumno=alumno)

    context = {'lista_cuotas': lista_cuotas,
               'alumno_es_argentino': alumno_es_argentino,
              }

    return render(request, 'sia/listado_cuotas.html', context)


@login_required
def generar_reporte(request):
    if not request.user.is_superuser:
        return redirect("sia:cuenta")

    cursados = Cursado.objects.filter()

    if request.method == 'POST':
        tipo_reporte = request.POST.get('tipo_reporte')
        cursado = Cursado.objects.get(id=request.POST.get('curso'))

        if tipo_reporte == "inscriptos":
            return generar_pdf(cursado)

        if tipo_reporte == "morosos":
            return reporte_morosos_pdf(cursado)

    context = {'lista_cursados': cursados}
    return render(request, 'sia/generar_reporte.html', context)


def inscribir_alumno(alumno, cursado):
    cursado.alumno.add(alumno)
    cursado.save()


def generar_cuotas(alumno, cursado):

    # Matrícula
    Cuota.objects.create(
        alumno=alumno,
        cursado=cursado,
        numero=0,
        valor_cuota_pesos=cursado.costo_inscripcion_pesos,
        valor_cuota_dolares=cursado.costo_inscripcion_dolares,
        es_inscripcion=True)

    # Generación de cuotas
    cantidad_cuotas = cursado.duracion
    for i in range(1, cantidad_cuotas + 1):
        Cuota.objects.create(
            alumno=alumno,
            cursado=cursado,
            numero=i,
            valor_cuota_pesos=cursado.valor_cuota_pesos,
            valor_cuota_dolares=cursado.valor_cuota_dolares)

    # Costo certificado
    Cuota.objects.create(
        alumno=alumno,
        cursado=cursado,
        numero=cantidad_cuotas + 1,
        valor_cuota_pesos=cursado.costo_certificado_pesos,
        valor_cuota_dolares=cursado.costo_certificado_dolares,
        es_certificado=True)


def es_argentino(alumno):
    return alumno.pais.nombre in ["Argentina", "argentina"]


def reporte_morosos_pdf(cursado):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="%s".pdf' % (cursado.nombre + " morosos")

    alto, ancho = A4
    doc = SimpleDocTemplate(response, pagesize=(ancho,alto))
    #doc.pagesize = portrait(A4)
    elements = []

    styles = getSampleStyleSheet()

    # Titulo página
    titulo = Paragraph(NOMBRE_CEFYT + ": Reporte morosos", styles["Heading2"])
    elements.append(titulo)

    # Cursado
    curso = Paragraph("Curso: " + str(cursado), styles["Normal"])
    elements.append(curso)

    # Fecha
    fecha = Paragraph("Fecha: " + time.strftime("%c"), styles["Normal"])
    elements.append(fecha)

    alumnos = []
    alumnos.append(['Apellido', 'Nombre', 'Nombre de usuario', 'Cuotas impagas'])
    for alumno in cursado.alumno.all():
        cuotas_impagas = Cuota.objects.filter(
                alumno=alumno,
                cursado=cursado,
                pagado=False)

        cuotas = ''
        for cuota in cuotas_impagas:
            if cuota.es_inscripcion:
                cuotas = 'Inscripción, ' + cuotas
            elif cuota.es_certificado:
                cuotas = 'Certificado, ' + cuotas
            else:
                cuotas = cuotas + str(cuota.numero) + ", "

        alumnos.append([alumno.usuario.last_name, alumno.usuario.first_name, alumno.usuario.username, cuotas])

    t = Table(alumnos)
    t.setStyle(TableStyle(
            [('BACKGROUND', (0, 0), (3, 0), colors.lavender),
             ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
    elements.append(t)


    doc.build(elements)

    return response

def generar_pdf(cursado):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="%s".pdf' % (cursado.nombre)

    alto, ancho = A4
    doc = SimpleDocTemplate(response, pagesize=(ancho,alto))
    #doc.pagesize = portrait(A4)
    elements = []

    styles = getSampleStyleSheet()

    # Titulo página
    titulo = Paragraph(NOMBRE_CEFYT, styles["Heading2"])
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
    alumnos.append(['Apellido', 'Nombre', 'Documento',
                    'País', 'Provincia', 'Localidad', 'Nombre de usuario'])
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

    alumno = obtener_alumno(request)
    cuota = Cuota.objects.get(id=request.POST.get('cuota'))

    cupon_valor = str('%.2f' % cuota.valor_cuota_pesos)

    # Generación del número cupón
    nro_gire = NUMERO_GIRE           # Valor fijo
    nro_cliente = '{:5d}'.format(alumno.id).replace(' ', '0')
    tipo_comprobante = "1"      # Tipo de comprobante: 1 dígito
    nro_comprobante ='{:6d}'.format(cuota.id).replace(' ', '0')
    importe = '{:7.2f}'.format(cuota.valor_cuota_pesos).replace('.', '').replace(' ', '0')
    anio_vencimiento = str(date.today().year)[2:]      # Año vencimiento: 2 dígitos
    mes_vencimiento = "12"      # Mes vencimiento: 2 dígitos
    dia_vencimiento = "31"      # Día vencimiento: 2 dígitos
    reservado = "0"             # Espacio reservado

    nro_cupon = nro_gire + nro_cliente + tipo_comprobante + nro_comprobante +\
        importe + anio_vencimiento + mes_vencimiento + dia_vencimiento +\
        reservado
    nro_cupon = str(nro_cupon)


    # Cálculo del dígito verificador
    SECUENCIA = "13579357935793579357935793579"
    suma = 0
    for i in range(len(nro_cupon)):
        suma += int(nro_cupon[i]) * int(SECUENCIA[i])

    digito_verificador = int(suma / 2) % 10
    digito_verificador = str(digito_verificador)
    nro_cupon += digito_verificador

    # Depuración
    lista_campos = [nro_gire, nro_cliente, tipo_comprobante, nro_comprobante, 
                    importe, anio_vencimiento, mes_vencimiento, dia_vencimiento, 
                    reservado, digito_verificador]

    depuracion = ' '
    depuracion = depuracion.join(lista_campos)

    # Nombre del archivo
    cupon = "Cupon"
    response['Content-Disposition'] = 'filename="%s".pdf' % (cupon)

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Imagen
    logo = Image('./sia/static/sia/cupon/logo.bmp')
    logo.drawHeight = 1.40*25.4*mm*logo.drawHeight / logo.drawWidth
    logo.drawWidth = 1.40*25.4*mm

    # Datos del cupón
    titulo1 = Paragraph("SEMINARIO VILLA CLARET", styles["Heading2"])
    titulo2 = Paragraph(NOMBRE_CEFYT, styles["Heading5"])

    apellido = alumno.usuario.last_name
    nombre = alumno.usuario.first_name
    domicilio = alumno.domicilio
    localidad = alumno.localidad
    provincia = alumno.provincia
    pais = alumno.pais.nombre

    if cuota.es_inscripcion:
        nro_cuota = "Inscripción "
    elif cuota.es_certificado:
        nro_cuota = "Certificado "
    else:
        nro_cuota = "Cuota número " + str(cuota.numero)

    cursado = "Curso: " + cuota.cursado.nombre
    valor_cuota = "$" + cupon_valor

    # Código barras
    tb = 0.254320987654 * mm  # thin bar
    bh = 20 * mm  # bar height
    bc = I2of5(
        nro_cupon, barWidth=tb, ratio=3, barHeight=bh, bearers=0,
        quiet=0, checksum=1)

    datos = [[logo, titulo1],
             ['', titulo2],
             ['', DOMICILIO_CEFYT + "."],
             ['', BARRIO_CEFYT + "."],
             ['', CODPOSTAL_CEFYT + ". " + LOCALIDAD_CEFYT + ", " + PAIS_CEFYT + "."],
             ['', CUIT_CEFYT  + "."],
             [],
             ['Señor/a:', apellido + ', ' + nombre],
             ['Domicilio:', domicilio + ', ' + localidad + ', ' + provincia + ', ' + pais],
             ['En concepto de:', nro_cuota],
             ['', Paragraph(cursado, styles['Normal'])],
             ['Total a pagar:', valor_cuota],
             [],
             [bc],
             [nro_cupon]
             ]

    t = Table(datos)
    t.setStyle(TableStyle([  # Logo
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

        ('GRID', (0, 0), (-1, -1), 1, colors.gray)]))

    elements.append(t)

    # d = Paragraph('Depuracion: ' + depuracion, styles["Heading5"])
    # elements.append(d)


    doc.build(elements)

    return response


#
# Procesamiento de pagos realizados por RapiPago.
#
@login_required
def procesar_pago(request):
    form = SubirArchivoForm()

    # Procesar archivo
    if request.method == 'POST':
        form = SubirArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_original, pagos = procesar_archivo(request.FILES['archivo'])
            context = {'archivo_original': archivo_original,
                       'pagos': pagos,
                       }

            return render(request, 'sia/procesar_pago.html', context)

    context = {'form': form}
    return render(request, 'sia/procesar_pago.html', context)



def procesar_archivo(archivo):
    """Procesa el archivo 'archivo' y retorna una tupla (original, pagos)

    Donde:
    'original': Es una lista ordenada que contiene cada fila del archivo.
    'pagos': Una lista que contiene 4-uplas de la forma:
             (cuota_id, alumno_id, fecha de pago, monto)
    """

    archivo_original = []
    pagos = []
    for fila in archivo:
        fila = str(fila)[:-5] # Se quita el prefijo b' y sufijo '/r/n
        archivo_original.append(fila)

        if fila[23:23+4] != NUMERO_GIRE:
            # Excluidos
            continue

        fecha_de_pago = "/".join([fila[6:6+2], fila[4:4+2], fila[0:4]])
        alumno_id = fila[27:27+5]
        cuota_id = fila[33:33+6]
        monto = fila[39:39+4] + "." + fila[43:43+2]
        pagos.append((cuota_id, alumno_id, fecha_de_pago, monto))

    return (archivo_original, pagos)

def obtener_alumno(request):
    usuario = User.objects.get(username=request.user.username)
    alumno = Alumno.objects.get(usuario=usuario)

    return alumno