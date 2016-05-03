# -*- coding: utf-8 -*-
from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *

from sia.models import Alumno, Cuota

from sia.CEFyT import *
import time


def generar_pdf(cursado):
    response = pdf_response(cursado.nombre)

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
        alumnos.append([alumno.usuario.last_name,
                        alumno.usuario.first_name,
                        alumno.documento,
                        alumno.pais,
                        alumno.provincia,
                        alumno.localidad,
                        alumno.usuario.username])
        cantidad_inscriptos = cantidad_inscriptos + 1

    numero_inscriptos = Paragraph(
        "Cantidad de inscriptos: " + str(cantidad_inscriptos), styles["Normal"])
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

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    doc.build(elements)

    return response


def reporte_cursos_inscriptos_alumno_pdf(cursado):
    response = pdf_response(cursado.nombre + " cursos por alumno")

    elements = []
    styles = getSampleStyleSheet()

    # Titulo página
    titulo = Paragraph(NOMBRE_CEFYT + ": Cursos inscriptos por alumnos", styles["Heading2"])
    elements.append(titulo)

    # Fecha
    fecha = Paragraph("Fecha: " + time.strftime("%c"), styles["Normal"])
    elements.append(fecha)

    # Datos
    datos = []
    datos.append(["Nombre alumnos (usuario)", "Cursos inscriptos"])
    for alumno in Alumno.objects.all().order_by('usuario__last_name'):
        cursos_inscriptos = ""
        for curso in alumno.cursado_set.all():
            cursos_inscriptos += "\"" + curso.nombre + "\"" + '<br />'

        alumno_nombre = alumno.usuario.last_name
        alumno_nombre += ", "
        alumno_nombre += alumno.usuario.first_name
        alumno_nombre = alumno_nombre.title()
        alumno_nombre += " ("
        alumno_nombre += alumno.usuario.username
        alumno_nombre += ")"
        datos.append([alumno_nombre, Paragraph(cursos_inscriptos, styles["Normal"])])

    t = Table(datos)
    t.setStyle(TableStyle(
            [('BACKGROUND', (0, 0), (3, 0), colors.lavender),
             ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
    elements.append(t)

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    doc.build(elements)

    return response


def reporte_morosos_pdf(cursado):
    response = pdf_response(cursado.nombre + " morosos")

    elements = []
    styles = getSampleStyleSheet()

    # Titulo página
    titulo = Paragraph(NOMBRE_CEFYT + ": Estado de deuda y recaudación", styles["Heading2"])
    elements.append(titulo)

    # Cursado
    curso = Paragraph("Curso: " + str(cursado), styles["Normal"])
    elements.append(curso)

    # Fecha
    fecha = Paragraph("Fecha: " + time.strftime("%c"), styles["Normal"])
    elements.append(fecha)

    # Datos
    total_recaudado_pesos = 0
    total_recaudado_dolares = 0
    cantidad_inscriptos = 0
    datos = []
    datos.append(["Alumno", "Estado", "Valor en pesos", "Valor en dólares"])
    for alumno in cursado.alumno.all().order_by('usuario__last_name'):
        cantidad_inscriptos += 1
        fila = []

        alumno_apellido = alumno.usuario.last_name.strip().title()
        alumno_nombre = alumno.usuario.first_name.strip().title()
        alumno_usuario = alumno.usuario.username.strip()
        id_alumno = alumno_apellido + ", " + alumno_nombre + " (" + alumno_usuario + ")"
        alumno_paragraph = Paragraph("<b>" + id_alumno + "</b>", styles["Normal"])
        fila.append(alumno_paragraph)
        datos.append(fila)

        fila = []
        inscripcion = Cuota.objects.filter(
            alumno=alumno,
            cursado=cursado,
            es_inscripcion=True,
            pagado=True)

        # Inscripción
        fila.append('Inscripción: ')
        temp = ''
        if inscripcion:
            temp += 'Fecha de pago: ' + str(inscripcion[0].fecha_de_pago)
            temp += '<br />'
            temp += 'Comprobante: ' + str(inscripcion[0].comprobante)
            fila.append(Paragraph(temp, styles["Normal"]))
            fila.append(inscripcion[0].valor_cuota_pesos)
            fila.append(inscripcion[0].valor_cuota_dolares)
            total_recaudado_pesos += inscripcion[0].valor_cuota_pesos
            total_recaudado_dolares += inscripcion[0].valor_cuota_dolares
        else:
            fila.append('No abonado')
            alumno_paragraph = Paragraph("", styles["Normal"])
            fila.append(alumno_paragraph)
        datos.append(fila)

        # Cuotas
        for cuota in Cuota.objects.filter(
            alumno=alumno,
            cursado=cursado,
            es_certificado=False,
            es_inscripcion=False).order_by('numero'):

            fila = []
            fila.append(Paragraph('Cuota nº: ' + str(cuota.numero), styles["Normal"]))
            temp = ''
            if cuota.pagado:
                temp += 'Fecha de pago: ' + str(cuota.fecha_de_pago)
                temp += '<br />'
                temp += 'Comprobante: ' + str(cuota.comprobante)
                fila.append(Paragraph(temp, styles["Normal"]))
                fila.append(cuota.valor_cuota_pesos)
                fila.append(cuota.valor_cuota_dolares)
                total_recaudado_pesos += cuota.valor_cuota_pesos
                total_recaudado_dolares += cuota.valor_cuota_dolares
            else:
                fila.append('No abonado')

            datos.append(fila)

        # Certificado
        fila = []
        fila.append(Paragraph('Certificado', styles["Normal"]))
        temp = ''
        certificado = Cuota.objects.filter(
            alumno=alumno,
            cursado=cursado,
            es_certificado=True,
            pagado=True)

        if certificado:
            temp += 'Fecha de pago: ' + str(certificado[0].fecha_de_pago)
            temp += '<br />'
            temp += 'Comprobante: ' + str(certificado[0].comprobante)
            fila.append(Paragraph(temp, styles["Normal"]))
            fila.append(certificado[0].valor_cuota_pesos)
            fila.append(certificado[0].valor_cuota_dolares)
            total_recaudado_pesos += certificado[0].valor_cuota_pesos
            total_recaudado_dolares += certificado[0].valor_cuota_dolares
        else:
            fila.append('No abonado')
        datos.append(fila)

    t = Table(datos)
    t.setStyle(TableStyle(
            [('BACKGROUND', (0, 0), (3, 0), colors.lavender),
             ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
    elements.append(t)

    # Total recaudado
    elements.append(Paragraph(
        "Cantidad inscriptos: " + str(cantidad_inscriptos), styles["Normal"]))
    elements.append(Paragraph(
        "Total recaudado $: " + str(total_recaudado_pesos), styles["Normal"]))
    elements.append(Paragraph(
        "Total recaudado u$s: " + str(total_recaudado_dolares), styles["Normal"]))

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    doc.build(elements)

    return response


def pdf_response(nombre_archivo):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="%s".pdf' % (nombre_archivo)

    return response
