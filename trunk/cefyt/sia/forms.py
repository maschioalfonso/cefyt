# -*- coding: utf-8 -*-
from django.forms import (ModelForm, PasswordInput, EmailField, CharField,
                          ModelChoiceField, IntegerField, DateField, Form, FileField)
from sia.models import Alumno, Pais
from django.db import models
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets


YEARS_CHOISES = tuple([str(year) for year in range(1920, 2015)])

class RegistroForm(ModelForm):
    nombre = CharField()
    apellido = CharField()
    email = EmailField(label="Correo electrónico")
    documento = IntegerField(label='Documento', min_value=1)
    password = CharField(widget=PasswordInput(), label="Contraseña")
    pais = ModelChoiceField(queryset=Pais.objects.all(),
                            empty_label=None, label='País')
    fecha_de_nacimiento = DateField(widget=SelectDateWidget(years=YEARS_CHOISES))

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


class SubirArchivoForm(Form):
    archivo = FileField()