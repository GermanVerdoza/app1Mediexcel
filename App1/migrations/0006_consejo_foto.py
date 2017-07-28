# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0005_auto_20170726_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='consejo',
            name='foto',
            field=models.ImageField(default=b'notfound.jpg', upload_to=b'App1/fotoJuegos'),
        ),
    ]
