# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sia', '0002_remove_cursado_descubrimiento_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='cursado',
            name='descubrimiento_curso',
            field=models.ForeignKey(to='sia.DescubrimientoCurso', default=0),
            preserve_default=False,
        ),
    ]
