# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from sia.forms import RegistroForm, alumno_desde_form
from sia.mail_template import SUBSCRIPTION_MAIL_BODY, SUBSCRIPTION_MAIL_SUBJECT
from sia.models import Alumno, Cursado, DescubrimientoOpcion, DescubrimientoCurso, Cuota, Noticia

from sia.reportes import reporte_cursos_inscriptos_alumno_pdf, reporte_morosos_pdf, generar_pdf


@login_required
def cuenta(request):
    if request.method == "GET" and request.user.is_superuser:
        return redirect("admin:index")

    alumno = obtener_alumno(request)
    noticias = Noticia.objects.all().order_by('-fecha')

    cursados = Cursado.objects.filter(
        inscripcion_abierta=True).exclude(alumno=alumno)
    cursados_inscripto = Cursado.objects.filter(alumno=alumno)

    opciones_descubrimiento = DescubrimientoOpcion.objects.all()

    if request.method == "POST":
        if cursados:

            cursado_seleccionado = 0
            for k, v in request.POST.items():
                if v == 'Inscribirse':
                    cursado_seleccionado = k

            cursado = Cursado.objects.get(id=cursado_seleccionado)

            # Inscripción y generación de cuotas
            inscribir_alumno(alumno, cursado)
            generar_cuotas(alumno, cursado)
            enviar_mail(alumno, cursado)

            # Envío de mail

        if opciones_descubrimiento:
            opcion = DescubrimientoOpcion.objects.get(
                id=request.POST.get('descubrimiento'))

            DescubrimientoCurso.objects.create(
                cursada=cursado,
                alumno=alumno,
                opcion=opcion)

        return redirect("sia:cuenta")

    context = {'lista_cursados': cursados,
               'lista_cursados_inscripto': cursados_inscripto,
               'opcion_descubrimiento': opciones_descubrimiento,
               'noticias': noticias}
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
                is_staff=True)
            if not creado:
                usuario_existente = True
            else:
                usuario.set_password(request.POST.get('password'))
                usuario.save()
                alumno_desde_form(form, usuario)

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
    lista_cuotas = Cuota.objects.filter(alumno=alumno)

    context = {'lista_cuotas': lista_cuotas}

    return render(request, 'sia/listado_cuotas.html', context)


@login_required
def generar_reporte(request):
    if not request.user.is_superuser:
        return redirect("sia:cuenta")

    cursados_activos = Cursado.objects.filter(
        inscripcion_abierta=True)
    cursados_inactivos = Cursado.objects.filter(
        inscripcion_abierta=False)

    if request.method == 'POST':
        tipo_reporte = request.POST.get('tipo_reporte')
        cursado = Cursado.objects.get(id=request.POST.get('curso'))

        if tipo_reporte == "inscriptos":
            return generar_pdf(cursado)

        if tipo_reporte == "morosos":
            return reporte_morosos_pdf(cursado)

        if tipo_reporte == "cursos_inscriptos_alumno":
            return reporte_cursos_inscriptos_alumno_pdf(cursado)

    # context = {'lista_cursados_activos': cursados_activos}
    # context = {'lista_cursados_inactivos': cursados_inactivos}
    context = {}
    context['lista_cursados_activos'] = cursados_activos
    context['lista_cursados_inactivos'] = cursados_inactivos

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


def enviar_mail(alumno, cursado):
    send_mail(
        SUBSCRIPTION_MAIL_SUBJECT.format(curso=cursado.nombre),
        SUBSCRIPTION_MAIL_BODY.format(curso=cursado.nombre),
        'noreply.cefyt@gmail.com',
        [alumno.usuario.username],
        fail_silently=True)


def obtener_alumno(request):
    usuario = User.objects.get(username=request.user.username)
    alumno = Alumno.objects.get(usuario=usuario)

    return alumno
