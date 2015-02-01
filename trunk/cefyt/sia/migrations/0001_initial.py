# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('documento', models.CharField(max_length=255)),
                ('fecha_de_nacimiento', models.DateField()),
                ('provincia', models.CharField(max_length=255)),
                ('localidad', models.CharField(max_length=255)),
                ('domicilio', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=255)),
                ('telefono_alter', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cuota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(default=0)),
                ('fecha_de_pago', models.DateField()),
                ('comprobante', models.CharField(max_length=255)),
                ('alumno', models.ForeignKey(to='sia.Alumno')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cursado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=255)),
                ('duracion', models.IntegerField(default=0)),
                ('costo_total_pesos', models.PositiveSmallIntegerField()),
                ('costo_total_dolares', models.PositiveSmallIntegerField()),
                ('costo_inscripcion_pesos', models.PositiveSmallIntegerField()),
                ('costo_inscripcion_dolares', models.PositiveSmallIntegerField()),
                ('inscripcion_abierta', models.BooleanField(default=False)),
                ('alumno', models.ManyToManyField(to='sia.Alumno', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DescubrimientoCurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opcion', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
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
