# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0002_comentario_encabezado'),
    ]

    operations = [
        migrations.AddField(
            model_name='juego',
            name='resumen',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
    ]
