from django.conf.urls import include, url
from wkhtmltopdf.views import PDFTemplateView
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'prueba1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index,name='index'),
    url(r'^Inicio$', views.index,name='index'),
    url(r'^login$', views.entrar,name='login'),
    url(r'^salir$', views.salir,name='salir'),
    url(r'^registro$', views.registro,name='registro'),
    url(r'^AgregarJuego$', views.agregar_juego,name='agregarjuego'),
    url(r'^AgregarConsejo$', views.agregar_consejo,name='agregarconsejo'),
    #url(r'^guardarJuego$', views.juego_guardado, name='juegoguardado'),
    url(r'^ConsultarJuegos$', views.ConsultaJuegos.as_view(), name='consultajuego'),
    url(r'^ConsultarConsejos$', view=views.ConsultaConsejos.as_view(), name='consultaconsejos'),
    url(r'^MejoresConsejos$', views.mejores_consejos,
        name='mejores'),
    url(r'^Detalle/(?P<idJuego>[0-9]+)/$', views.ver_juego, name='vistaJuego'),
    url(r'^Consejos/(?P<idConsejo>[0-9]+)/$', views.ver_consejo, name='vistaConsejo'),
    url(r'^perfil/(?P<userid>[0-9]+)/$', views.perfil, name='perfil'),
    url(r'^votar/(?P<consejoId>[0-9]+)/$', views.voto, name='votar'),
    url(r'^MejoresPDF$', view=views.MejorPdf.as_view(),
        name='mejorPdf'),
]
