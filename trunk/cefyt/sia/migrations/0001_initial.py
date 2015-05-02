# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('usuario_aula_virtual', models.CharField(max_length=255, blank=True, null=True)),
                ('documento', models.CharField(max_length=255)),
                ('fecha_de_nacimiento', models.DateField()),
                ('provincia', models.CharField(max_length=255)),
                ('localidad', models.CharField(max_length=255)),
                ('domicilio', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=255)),
                ('telefono_alter', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Alumnos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cuota',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('numero', models.IntegerField(default=0)),
                ('fecha_de_pago', models.DateField(blank=True, null=True)),
                ('comprobante', models.CharField(max_length=255, blank=True, null=True)),
                ('descripcion', models.CharField(max_length=255, blank=True, null=True)),
                ('pagado', models.BooleanField(default=False)),
                ('costo_certificado_dolares', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('costo_certificado_pesos', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('valor_cuota_pesos', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('valor_cuota_dolares', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('alumno', models.ForeignKey(to='sia.Alumno')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cursado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('duracion', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('costo_inscripcion_pesos', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('costo_inscripcion_dolares', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('costo_certificado_pesos', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('costo_certificado_dolares', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('valor_cuota_pesos', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('valor_cuota_dolares', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('inscripcion_abierta', models.BooleanField(default=False)),
                ('alumno', models.ManyToManyField(to='sia.Alumno', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Cursados',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Cursos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DescubrimientoCurso',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('alumno', models.ForeignKey(to='sia.Alumno')),
                ('cursada', models.ForeignKey(to='sia.Cursado')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DescubrimientoOpcion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('opcion', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Descubrimiento opciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Materias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Paises',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='descubrimientocurso',
            name='opcion',
            field=models.ForeignKey(to='sia.DescubrimientoOpcion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='curso',
            name='materias',
            field=models.ManyToManyField(to='sia.Materia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cursado',
            name='curso',
            field=models.ForeignKey(to='sia.Curso'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cuota',
            name='cursado',
            field=models.ForeignKey(to='sia.Cursado'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumno',
            name='pais',
            field=models.ForeignKey(to='sia.Pais'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumno',
            name='usuario',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
