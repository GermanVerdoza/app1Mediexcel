from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, HTML, Submit,Reset
from django.forms import ModelForm
from django import forms
from App1.models import Juego,Consejo,Comentario

class FormJuego(ModelForm):
    #foto = forms.ImageField(required=True)
    class Meta:
        model=Juego
        exclude = ('usuario',)
        widgets = {'fecha':forms.DateInput(attrs={'type':'date'})}


class FormConsejo(ModelForm):
    class Meta:
        model=Consejo
        fields=['titulo','descripcion']


class FormComentario(ModelForm):
    class Meta:
        model=Comentario
        fields=['encabezado','cuerpo']


class FormLogin(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=12,widget=forms.PasswordInput)


class FormConsejoCryspy(forms.ModelForm):
    class Meta:
        model = Consejo
        fields = ['juego','titulo','descripcion']

    def __init__(self, *args, **kwargs):
        super(FormConsejoCryspy, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Fieldset(u'Juego al que pertenece',
                                             HTML('<div '
                                                  'class="card-header"><code>'
                                                  'Elija el juego en el cual quiera registrar el consejo</code>'
                                                  '</div>'),
                                             Field('juego',
                                                   wrapper_class='col-md-6')),
                                    Fieldset(u'Datos del consejo',
                                             Field('titulo',
                                                   wrapper_class='card '
                                                                 'col-md-3',
                                                   title='Elige un nombre '
                                                         'clave para el '
                                                         'consejo'
                                                   ),
                                             Field('descripcion',
                                                   wrapper_class='card '
                                                                 'col-md-3'),
                                             css_class='card-columns mb-3'),
                                    Submit('submit','GUARDAR',css_class='btn '
                                                                  'btn-success'),Reset('reset','Limpiar'),)
        self.fields['juego'].label = 'Nombre del Juego'
        self.fields['titulo'].label = 'Titulo del consejo'
        self.fields['descripcion'].label = 'Descripcion del consejo'
