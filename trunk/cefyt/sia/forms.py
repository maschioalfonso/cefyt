from django.forms import ModelForm, PasswordInput, Form, EmailField, CharField, ModelChoiceField, TextInput, IntegerField
from django.contrib.auth.models import User
from sia.models import Alumno, Pais


class RegistroForm(ModelForm):
    nombre = CharField()
    apellido = CharField()
    email = EmailField(label="e-mail")
    documento = IntegerField(label='Documento', min_value=1)
    password = CharField(widget=PasswordInput(),label="Contrasena")
    pais = ModelChoiceField(queryset=Pais.objects.all(), empty_label=None, label='Pais')

    
    class Meta:
        model = Alumno
        exclude = ['usuario']
        fields = ['nombre',
                  'apellido',
                  'email',
                  'documento',
                  'domicilio',
                  'pais',
                  'provincia',
                  'localidad',
                  'telefono',
                  'telefono_alter',
                  'fecha_de_nacimiento',
                 ]

        labels = {'nombre' : 'Nombre',
                  'apellido' : 'Apellido',
                  'documento' : 'Nro. de documento',
                  'domicilio' : 'Domicilio',
                  'provincia' : 'Provincia',
                  'localidad' : 'Localidad',
                  'telefono' : "Telefono",
                  'telefono_alter' : 'Telefono alternativo',
                  'fecha_de_nacimiento' : 'Fecha de nacimiento',
                 }
