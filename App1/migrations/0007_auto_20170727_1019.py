# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0006_consejo_foto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consejo',
            name='foto',
        ),
        migrations.AddField(
            model_name='juego',
            name='foto',
            field=models.ImageField(default=b'notfound.jpg', upload_to=b'App1/fotoJuegos'),
        ),
    ]
