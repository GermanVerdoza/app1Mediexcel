from django.http import  HttpResponse
from django.views.generic import  ListView,TemplateView
from django.views.generic.base import View
from wkhtmltopdf.views import PDFTemplateResponse,PDFTemplateView
from django.db.models import Count
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404, redirect, \
    render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from App1.form import FormComentario,FormJuego,FormConsejo,FormLogin, FormConsejoCryspy
from django.contrib.auth.decorators import login_required
from  App1.models import Juego,Consejo,Comentario,Voto
# Create your views here.


def index(request):
    return render_to_response('inicio.html',context_instance=RequestContext(request))


@login_required()
def agregar_juego(request):
    if request.method == 'POST':
        regresar = reverse('consultajuego')
        form = FormJuego(request.POST,request.FILES)
        if form.is_valid():
            print request.user
            juego = form.save(commit=False)
            juego.usuario = request.user
            juego.save()
            return render(request,'juegoGuardado.html',{'accion':'exito',
                                                        'clave':'Juego',
                                                        'regresar':regresar})
        else:
            return render(request,'agregarJuego.html',{'form':form})
    else:
        form = FormJuego()

    return render(request,'agregarJuego.html',{'form':form})


# def juego_guardado(request):
#     return render(request,'juegoGuardado.html',{'accion':'exito'})


@login_required()
def ver_juego(request,idJuego):
    detalle = get_object_or_404(Juego, pk=idJuego)
    if not detalle:
        return render_to_response('404.html',{'objeto':'Juego',
                                              'regresar':reverse('index')},\
               context_instance=RequestContext(request))
    consejos = Consejo.objects.filter(juego=idJuego)
    regresar = reverse('vistaJuego',args=[detalle.id])
    anchoframe=detalle.foto.width + 40
    if request.method == 'POST':
        form = FormConsejo(request.POST)
        if form.is_valid():
            consejo = form.save(commit=False)
            consejo.usuario = request.user
            consejo.juego_id = idJuego
            consejo.save()
            return render(request,'juegoGuardado.html',{'detalle':detalle,
                                                        'accion':'exito',
                                                        'clave':'Consejo',
                                                        'regresar':regresar})
    else:
        form=FormConsejo()
    return render(request,'verJuego.html',{'detalle':detalle,
                                           'consejos':consejos,'form':form,
                                           'anchoframe':anchoframe})

@login_required()
def ver_consejo(request,idConsejo):
    try:
        detalle = Consejo.objects.get(pk=idConsejo)
    except Consejo.DoesNotExist:
        return render_to_response('404.html',{'objeto':'Consejo',
                                              'regresar':reverse('index')},\
               context_instance=RequestContext(request))
    comentarios = Comentario.objects.filter(consejo=idConsejo)
    votos = Consejo.objects.get(pk=idConsejo).voto_set.all().count()
    regresar = reverse('vistaConsejo',args=[detalle.id])
    ya_votado=get_object_or_404(Consejo,pk=idConsejo).voto_set.\
                  filter(user=request.user) and True or False
    if request.method == 'POST':
        form = FormComentario(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.consejo_id = idConsejo
            comentario.save()
            return render(request,'juegoGuardado.html',{'detalle':detalle,
                                                        'accion':'exito',
                                                        'clave':'Comentario',
                                                        'regresar':regresar})
    else:
        form=FormComentario()
    return render(request,'verConsejo.html',{'detalle':detalle,
                                             'comentarios':comentarios,
                                             'form':form,'votos':votos,
                                             'ya_votado':ya_votado})


def entrar(request):
    message = None
    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    message = 'Te has identificado de modo correcto'
                else:
                    message = 'Tu usuario esta inactivo'
            else:
                message = 'Nombre de usuario y/o password incorrecto'
    else:
        form = FormLogin()
    return render_to_response('login.html',{'mensaje':message,'form':form},
                              context_instance=RequestContext(request))

def salir(request):
    logout(request)
    return redirect('index')


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print form
        if form.is_valid():
            form.save()
            print form
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('index',permanent=True)
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form},
                  context_instance=RequestContext(request))

def perfil(request,userid):
    juegos = Juego.objects.filter(usuario_id=userid).count()
    consejos = Consejo.objects.filter(usuario_id=userid).count()
    comentarios = Comentario.objects.filter(usuario_id=userid).count()
    usuario = User.objects.get(pk=userid)
    return render_to_response('estadisticas.html',{'usuario':usuario,
                                                   'juegos':juegos,
                                                   'consejos':consejos,
                                                   'comentarios':comentarios},
                              context_instance=RequestContext(request))


def mejores_consejos(request):
    lista = Consejo.objects.select_related('juego').values('juego__nombre',
                                                           'titulo','id').\
        prefetch_related('consejo_set__voto_set').annotate(votos=Count(
        'voto')).order_by('-votos').filter(mejor=True)
    return render(request,'mejores.html',{'lista':lista},
                  context_instance=RequestContext(request))


def voto(request, consejoId):
    new_like, created = Voto.objects.get_or_create(user=request.user,
                                                   consejo_id=consejoId)
    if not created:
        return HttpResponse('Ya has votado este consejo')
    else:
        consejo = Consejo.objects.get(pk=consejoId)
        consejo.es_mejor(consejo.juego_id)
        return redirect('vistaConsejo',consejoId,permanent=True)


class ConsultaConsejos(ListView):
    model = Consejo
    template_name = 'consultaConsejos.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = Consejo.objects.all().order_by('juego_id')
        return queryset


class ConsultaJuegos(ListView):
    model = Juego
    template_name = 'consultaJuegos.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = Juego.objects.all().order_by('nombre')
        return queryset


class MejorPdf(PDFTemplateView):
    show_content_in_browser = True
    template_name = 'mejorPDF.html'
    filename = 'MejoresConsejos.pdf'
    cmd_options = {
        'margin-top': 4.3,  # 4.2mm
        'margin-right': 1.5,
        'margin-bottom': 0,
        'margin-left': 1.5,
        'page-size': 'Letter',
    }

    def get_context_data(self, **kwargs):
        context = super(MejorPdf,
                        self).get_context_data(**kwargs)
        query = Consejo.objects.select_related('juego').values('juego__nombre',
                                                           'titulo', 'id'). \
        prefetch_related('consejo_set__voto_set').annotate(votos=Count(
        'voto')).order_by('-votos').filter(mejor=True)
        print query
        context.update({
            'lista': query
        })
        return context

    def get(self, request, *args, **kwargs):
        response = super(MejorPdf, self).get(request, *args, **kwargs)
        return response



@login_required()
def agregar_consejo(request):
    if request.method == 'POST':
        regresar = reverse('consultaconsejos')
        form = FormConsejoCryspy(request.POST)
        if form.is_valid():
            print request.user
            juego = form.save(commit=False)
            juego.usuario = request.user
            juego.save()
            return render(request,'juegoGuardado.html',{'accion':'exito',
                                                        'clave':'Consejo',
                                                        'regresar':regresar})
        else:
            return render_to_response('agregarConsejo.html',{'form':form},
                                      context_instance=RequestContext(request))
    else:
        form = FormConsejoCryspy()

    return render_to_response('agregarConsejo.html',{'form':form},
                                      context_instance=RequestContext(request))