# -*- coding: utf-8 -*-
from django.forms import (ModelForm, PasswordInput, EmailField, CharField,
                          ModelChoiceField, IntegerField)
from sia.models import Alumno, Pais


class RegistroForm(ModelForm):
    nombre = CharField()
    apellido = CharField()
    email = EmailField(label="Correo electrónico")
    documento = IntegerField(label='Documento', min_value=1)
    password = CharField(widget=PasswordInput(), label="Contraseña")
    pais = ModelChoiceField(queryset=Pais.objects.all(),
                            empty_label=None, label='País')

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
