# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('apellido', models.CharField(max_length=20)),
                ('nombres', models.CharField(max_length=25)),
                ('documento', models.CharField(max_length=12)),
                ('fecha_de_nacimiento', models.DateField()),
                ('provincia', models.CharField(max_length=20)),
                ('localidad', models.CharField(max_length=20)),
                ('domicilio', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=25)),
                ('telefono_alter', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=75, serialize=False, primary_key=True)),
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
                ('comprobante', models.CharField(max_length=10)),
                ('alumno', models.ForeignKey(to='sia.Alumno')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cursado',
            fields=[
                ('nombre', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('duracion', models.IntegerField(default=0)),
                ('costo_total_pesos', models.DecimalField(max_digits=7, decimal_places=2)),
                ('costo_total_dolares', models.DecimalField(max_digits=7, decimal_places=2)),
                ('costo_inscripcion_pesos', models.DecimalField(max_digits=7, decimal_places=2)),
                ('costo_inscripcion_dolares', models.DecimalField(max_digits=7, decimal_places=2)),
                ('inscripcion_abierta', models.BooleanField(default=False)),
                ('alumno', models.ManyToManyField(to='sia.Alumno', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('nombre', models.CharField(max_length=30, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('nombre', models.CharField(max_length=30, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=12)),
            ],
            options={
            },
            bases=(models.Model,),
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
    ]
