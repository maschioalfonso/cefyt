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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('documento', models.CharField(max_length=255)),
                ('fecha_de_nacimiento', models.DateField()),
                ('provincia', models.CharField(max_length=255)),
                ('localidad', models.CharField(max_length=255)),
                ('domicilio', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=255)),
                ('telefono_alter', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cuota',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombre', models.CharField(unique=True, max_length=255)),
                ('duracion', models.IntegerField(default=0)),
                ('costo_total_pesos', models.DecimalField(max_digits=7, decimal_places=2)),
                ('costo_total_dolares', models.DecimalField(max_digits=7, decimal_places=2)),
                ('costo_inscripcion_pesos', models.DecimalField(max_digits=7, decimal_places=2)),
                ('costo_inscripcion_dolares', models.DecimalField(max_digits=7, decimal_places=2)),
                ('inscripcion_abierta', models.BooleanField(default=False)),
                ('alumno', models.ManyToManyField(to='sia.Alumno', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('nombre', models.CharField(primary_key=True, serialize=False, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DescubrimientoCurso',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('opcion', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('nombre', models.CharField(primary_key=True, serialize=False, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
