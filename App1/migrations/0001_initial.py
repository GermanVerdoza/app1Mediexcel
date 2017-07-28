# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuerpo', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Consejo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('votos', models.IntegerField(default=0)),
                ('mejor', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Juego',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('fecha', models.DateField(verbose_name=b'Fecha de Lanzamiento')),
                ('genero', models.CharField(max_length=200, choices=[(b'Plataformas', b'Plataformas'), (b'FPS', b'Disparos en primera Persona'), (b'RPG', b'Juegos del rol'), (b'Luchas', b'Luchas (Combates)'), (b'Carreras', b'Carreras'), (b'Deportes', b'Deportes')])),
                ('jugadores', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('apellidos', models.CharField(max_length=300)),
                ('correo', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=12)),
            ],
        ),
        migrations.AddField(
            model_name='juego',
            name='usuario',
            field=models.ForeignKey(to='App1.Usuario'),
        ),
        migrations.AddField(
            model_name='consejo',
            name='juego',
            field=models.ForeignKey(to='App1.Juego'),
        ),
        migrations.AddField(
            model_name='consejo',
            name='usuario',
            field=models.ForeignKey(to='App1.Usuario'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='consejo',
            field=models.ForeignKey(to='App1.Consejo'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(to='App1.Usuario'),
        ),
    ]
