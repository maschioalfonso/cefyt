

from django.forms import ModelForm, Form, EmailField, CharField, ModelChoiceField
from django.contrib.auth.models import User

from sia.models import Alumno, Pais


# Create the form class.
class UsuarioForm(ModelForm):

#	def __init__():
#		username = super(, help_text='')

    class Meta:
    	model = User
    	#fields = ['username', 'password']


class RegistroForm(ModelForm):
    nombre = CharField()
    apellido = CharField()
    email = EmailField()
    password = CharField()
    pais = ModelChoiceField(queryset=Pais.objects.all(), empty_label=None)

    class Meta:
        model = Alumno
        exclude = ['usuario']
        #fields = ['nombre', 'apellido', 'email', 'pais']