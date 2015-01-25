# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sia', '0003_cursado_descubrimiento_curso'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescubrimientoOpcion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('opcion', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='cursado',
            name='descubrimiento_curso',
        ),
        migrations.AddField(
            model_name='descubrimientocurso',
            name='alumno',
            field=models.ForeignKey(default=None, to='sia.Alumno'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='descubrimientocurso',
            name='cursada',
            field=models.ForeignKey(default=None, to='sia.Cursado'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='descubrimientocurso',
            name='opcion',
            field=models.ForeignKey(to='sia.DescubrimientoOpcion'),
            preserve_default=True,
        ),
    ]
