from django.db import models
from django.db.models import IntegerField, Model
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
MAX_LENGTH = 255


class Pais(models.Model):

    class Meta:
        verbose_name_plural = "Paises"

    nombre = models.CharField(unique=True, max_length=MAX_LENGTH)

    def __str__(self):              # __unicode__ on Python 2
        return self.nombre


class Alumno(models.Model):

    class Meta:
        verbose_name_plural = "Alumnos"

    usuario = models.OneToOneField(User)
    documento = models.CharField(max_length=MAX_LENGTH)
    fecha_de_nacimiento = models.DateField()
    pais = models.ForeignKey("Pais")
    provincia = models.CharField(max_length=MAX_LENGTH)
    localidad = models.CharField(max_length=MAX_LENGTH)
    domicilio = models.CharField(max_length=MAX_LENGTH)
    telefono = models.CharField(max_length=MAX_LENGTH)
    telefono_alter = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.usuario.username


class Materia(models.Model):

    class Meta:
        verbose_name_plural = "Materias"

    nombre = models.CharField(unique=True, max_length=MAX_LENGTH)

    def __str__(self):              # __unicode__ on Python 2
        return self.nombre


class Curso(models.Model):

    class Meta:
        verbose_name_plural = "Cursos"

    nombre = models.CharField(unique=True, max_length=MAX_LENGTH)
    materias = models.ManyToManyField(Materia)
    descripcion = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.nombre


class Cursado(models.Model):

    class Meta:
        verbose_name_plural = "Cursados"

    nombre = models.CharField(unique=True, max_length=MAX_LENGTH)
    curso = models.ForeignKey(Curso)
    alumno = models.ManyToManyField(Alumno, blank=True, null=True)
    duracion = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(12)]) #Restringir de 1 a 12. CHOICES de 1 a 12 !
    # duracion = models.IntegerField(default=0, choices=[(x, x) for x in range(0,12)])
    costo_inscripcion_pesos = models.DecimalField( decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    costo_inscripcion_dolares = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    costo_certificado_pesos = models.DecimalField( decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    costo_certificado_dolares = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    valor_cuota_pesos = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    valor_cuota_dolares = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    inscripcion_abierta = models.BooleanField(default=False)

    def __str__(self):              # __unicode__ on Python 2
        return self.nombre


class DescubrimientoOpcion(models.Model):

    class Meta:
        verbose_name_plural = "Descubrimiento opciones"

    opcion = models.CharField(unique=True, max_length=MAX_LENGTH)

    def __str__(self):              # __unicode__ on Python 2
        return self.opcion


class DescubrimientoCurso(models.Model):

    cursada = models.ForeignKey(Cursado)
    alumno = models.ForeignKey(Alumno)
    opcion = models.ForeignKey(DescubrimientoOpcion)

    def __str__(self):              # __unicode__ on Python 2
        return self.alumno.usuario.username + ' - ' + self.cursada.nombre + '-> ' + self.opcion.opcion


class Cuota(models.Model):

    alumno = models.ForeignKey(Alumno)
    cursado = models.ForeignKey(Cursado)
    numero = models.IntegerField(default=0)
    fecha_de_pago = models.DateField(blank=True, null=True)
    comprobante = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    descripcion = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    pagado = models.BooleanField(default=False)
    costo_certificado_dolares = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    costo_certificado_pesos = models.DecimalField( decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    valor_cuota_pesos = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    valor_cuota_dolares = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])

    def __str__(self):              # __unicode__ on Python 2
        etiqueta = self.alumno.usuario.first_name + ': ' + self.cursado.nombre + ' - ' + 'Cuota: ' + str(self.numero)
        return etiqueta
