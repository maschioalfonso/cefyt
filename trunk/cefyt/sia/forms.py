# -*- coding: utf-8 -*-
from django.forms import (ModelForm, PasswordInput, EmailField, CharField,
                          ModelChoiceField, IntegerField, DateField, Form, FileField)
from sia.models import Alumno, Pais
from django.forms.extras.widgets import SelectDateWidget


YEARS_CHOICES = tuple([str(year) for year in range(1920, 2015)])


class RegistroForm(ModelForm):
    nombre = CharField()
    apellido = CharField()
    email = EmailField(label="Correo electrónico")
    documento = IntegerField(label='Documento', min_value=1)
    password = CharField(widget=PasswordInput(), label="Contraseña")
    pais = ModelChoiceField(queryset=Pais.objects.all(), empty_label=None, label='País')
    fecha_de_nacimiento = DateField(widget=SelectDateWidget(years=YEARS_CHOICES))

    class Meta:
        model = Alumno
        exclude = ['usuario']
        fields = ['nombre',
                  'apellido',
                  'documento',
                  'domicilio',
                  'pais',
                  'provincia',
                  'localidad',
                  'telefono',
                  'telefono_alter',
                  'fecha_de_nacimiento',
                  'email']

        labels = {'nombre': 'Nombre',
                  'apellido': 'Apellido',
                  'documento': 'Nro. de documento',
                  'domicilio': 'Domicilio',
                  'provincia': 'Provincia',
                  'localidad': 'Localidad',
                  'telefono': "Teléfono",
                  'telefono_alter': 'Teléfono alternativo',
                  'fecha_de_nacimiento': 'Fecha de nacimiento'}


def alumno_desde_form(form, usuario):
    """
    Crea un nuevo Alumno a partir de un RegistroForm.

    Precondición:
        form.is_valid()
    """

    alumno = Alumno(
        usuario=usuario,
        documento=form.cleaned_data.get('documento'),
        pais=form.cleaned_data.get('pais'),
        fecha_de_nacimiento=form.cleaned_data.get('fecha_de_nacimiento'),
        provincia=form.cleaned_data.get('provincia'),
        localidad=form.cleaned_data.get('localidad'),
        domicilio=form.cleaned_data.get('domicilio'),
        telefono=form.cleaned_data.get('telefono'),
        telefono_alter=form.cleaned_data.get('telefono_alter'))
    alumno.save()

    return alumno


class SubirArchivoForm(Form):
    archivo = FileField()
