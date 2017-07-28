from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

GENEROS=(('Plataformas','Plataformas'),('FPS','Disparos en primera Persona'),
         ('RPG','Juegos del rol'),('Luchas','Luchas (Combates)'),
         ('Carreras','Carreras'),('Deportes','Deportes'))

# Create your models here.


class Juego(models.Model):
    nombre = models.CharField(max_length=200)
    resumen = models.TextField()
    foto = models.ImageField(upload_to='App1/fotoJuegos',default='notfound.jpg')
    fecha = models.DateField('Fecha de Lanzamiento')
    genero = models.CharField(max_length=200,choices=GENEROS)
    jugadores = models.IntegerField()
    usuario = models.ForeignKey(User)

    def __str__(self):
        return self.nombre


class Consejo(models.Model):
    juego=models.ForeignKey(Juego)
    titulo=models.CharField(max_length=200)
    descripcion=models.TextField()
    mejor=models.BooleanField(default=False)
    usuario=models.ForeignKey(User)

    def __str__(self):
        return self.titulo

    def es_mejor(self,juegoId):
        list = Consejo.objects.filter(juego_id=juegoId).annotate(votos=Count('voto')).order_by('-votos')
        for c in list:
            if c.titulo == self.titulo:
                c.mejor = True
                c.save(update_fields=['mejor'])
            else:
                c.mejor = False
                c.save(update_fields=['mejor'])




class Comentario(models.Model):
    consejo=models.ForeignKey(Consejo)
    usuario=models.ForeignKey(User)
    encabezado=models.CharField(max_length=200)
    cuerpo=models.TextField()

    def __str__(self):
        return self.encabezado

class Voto(models.Model):
    user = models.ForeignKey(User)
    consejo = models.ForeignKey(Consejo)
    created = models.DateTimeField(auto_now_add=True)