from django.db import models

MAX_LENGTH = 255
class Pais(models.Model):
    nombre = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):              # __unicode__ on Python 2
        return self.nombre

class Alumno(models.Model):
    apellido = models.CharField(max_length=20)
    nombres = models.CharField(max_length=25)
    documento = models.CharField(max_length=12)
    fecha_de_nacimiento = models.DateField()
    pais = models.ForeignKey(Pais)
    provincia = models.CharField(max_length=20)
    localidad = models.CharField(max_length=20)
    domicilio = models.CharField(max_length=50)
    telefono = models.CharField(max_length=25)
    telefono_alter = models.CharField(max_length=25)
    email = models.EmailField(primary_key=True)

    def __str__(self):              # __unicode__ on Python 2
        etiqueta = self.apellido + ' - ' + self.nombres 
        return etiqueta


class Materia(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.nombre


class Curso(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    materias = models.ManyToManyField(Materia)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.nombre


class Cursado(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    curso = models.ForeignKey(Curso)
    alumno = models.ManyToManyField(Alumno, blank=True, null=True)
    duracion = models.IntegerField(default=0) #Restringir de 1 a 12. CHOICES de 1 a 12 !
    # duracion = models.IntegerField(default=0, choices=[(x, x) for x in range(0,12)])

    costo_total_pesos = models.DecimalField(max_digits=7, decimal_places=2)
    costo_total_dolares = models.DecimalField(max_digits=7, decimal_places=2)
    costo_inscripcion_pesos = models.DecimalField(max_digits=7, decimal_places=2)
    costo_inscripcion_dolares = models.DecimalField(max_digits=7, decimal_places=2)
    inscripcion_abierta = models.BooleanField(default=False)

    def __str__(self):              # __unicode__ on Python 2
        return self.nombre
        
class Cuota(models.Model):
    alumno = models.ForeignKey(Alumno)
    cursado = models.ForeignKey(Cursado)
    numero = models.IntegerField(default=0)
    fecha_de_pago = models.DateField()
    comprobante = models.CharField(max_length=10)
    
    def __str__(self):              # __unicode__ on Python 2
        etiqueta = self.alumno.apellido + ': ' + self.cursado.nombre + ' - ' + 'Cuota: ' + str(self.numero)
        return etiqueta