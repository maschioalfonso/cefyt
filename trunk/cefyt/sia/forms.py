

from django.forms import ModelForm
from django.contrib.auth.models import User


# Create the form class.
class UsuarioForm(ModelForm):

#	def __init__():
#		username = super(, help_text='')

    class Meta:
    	model = User
    	#fields = ['username', 'password']