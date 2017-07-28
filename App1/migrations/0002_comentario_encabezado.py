# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='encabezado',
            field=models.CharField(default='Comentario', max_length=200),
            preserve_default=False,
        ),
    ]
