# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cursado',
            name='id',
            field=models.AutoField(verbose_name='ID', default=0, auto_created=True, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cursado',
            name='nombre',
            field=models.CharField(unique=True, max_length=255),
            preserve_default=True,
        ),
    ]
