from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
MAX_LENGTH = 255


class Pais(models.Model):
    nombre = models.CharField(unique=True, max_length=MAX_LENGTH)

    class Meta:
        verbose_name_plural = "Paises"

    def __str__(self):
        return self.nombre


class Alumno(models.Model):
    usuario = models.OneToOneField(User)
    usuario_aula_virtual = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True)
    documento = models.CharField(max_length=MAX_LENGTH)
    fecha_de_nacimiento = models.DateField()
    pais = models.ForeignKey("Pais")
    provincia = models.CharField(max_length=MAX_LENGTH)
    localidad = models.CharField(max_length=MAX_LENGTH)
    domicilio = models.CharField(max_length=MAX_LENGTH)
    telefono = models.CharField(max_length=MAX_LENGTH)
    telefono_alter = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Alumnos"

    def __str__(self):
        return self.usuario.username


class Materia(models.Model):
    nombre = models.CharField(unique=True, max_length=MAX_LENGTH)

    class Meta:
        verbose_name_plural = "Materias"

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    nombre = models.CharField(unique=True, max_length=MAX_LENGTH)
    materias = models.ManyToManyField(Materia)
    descripcion = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nombre


class Cursado(models.Model):
    nombre = models.CharField(unique=True, max_length=MAX_LENGTH)
    curso = models.ForeignKey(Curso)
    alumno = models.ManyToManyField(Alumno, blank=True, null=True)
    duracion = models.IntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(12)])
    costo_inscripcion_pesos = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    costo_inscripcion_dolares = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    costo_certificado_pesos = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    costo_certificado_dolares = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    valor_cuota_pesos = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    valor_cuota_dolares = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    inscripcion_abierta = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Cursados"

    def __str__(self):
        return self.nombre


class DescubrimientoOpcion(models.Model):
    opcion = models.CharField(unique=True, max_length=MAX_LENGTH)

    class Meta:
        verbose_name_plural = "Descubrimiento opciones"

    def __str__(self):
        return self.opcion


class DescubrimientoCurso(models.Model):
    cursada = models.ForeignKey(Cursado)
    alumno = models.ForeignKey(Alumno)
    opcion = models.ForeignKey(DescubrimientoOpcion)

    def __str__(self):
        return self.alumno.usuario.username + ' - ' + \
               self.cursada.nombre + '-> ' + self.opcion.opcion


class Cuota(models.Model):
    alumno = models.ForeignKey(Alumno)
    cursado = models.ForeignKey(Cursado)
    numero = models.IntegerField(default=0)
    fecha_de_pago = models.DateField(blank=True, null=True)
    comprobante = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True)
    descripcion = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True)
    pagado = models.BooleanField(default=False)
    costo_certificado_dolares = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    costo_certificado_pesos = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    valor_cuota_pesos = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    valor_cuota_dolares = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.alumno.usuario.first_name + ': ' +\
               self.cursado.nombre + ' - ' + 'Cuota: ' + str(self.numero)
