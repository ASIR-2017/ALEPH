#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import *
from datetime import datetime, timedelta, date
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.admin import widgets
from django.forms import ValidationError
from .widgets import *
from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import AuthenticationForm
from django.forms import extras
from django.contrib.admin.widgets import FilteredSelectMultiple, AdminDateWidget
from dal import autocomplete

########################################
# Formulario de login
########################################

class LoginForm(AuthenticationForm):
    username = forms.CharField(label = "Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label = "Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


########################################
#Formularios para crear objetos o modificarlos
#utilizando crispy-forms
########################################

class ArqueologiaForm(forms.ModelForm): 
    objetos_relacionados = forms.ModelMultipleChoiceField(
        queryset=Arqueologia.objects.extra(select={'n': "cast(split_part(numinv,'/',1) as integer)",'l': "char_length(numinv)",'e': "split_part(numinv,'/',2)"},order_by=['n','l','e']),
        widget=autocomplete.ModelSelect2Multiple(url='arqueologia-autocomplete'),
        required=False
    )

    material = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        widget=ModelSelect2MultipleWithPop(url='material-autocomplete'),
        label="Materiales",
        required=False
    )

    bibliografia = forms.ModelMultipleChoiceField(
        queryset=Bibliografia.objects.all(),
        widget=ModelSelect2MultipleWithPop(url='bibliografia-autocomplete'),
        label="Bibliografía",
        required=False
    )
    
    ubicacion = forms.ModelChoiceField(
        queryset=Ubicacion.objects.all(),
        widget=ModelSelect2WithPop(url='ubicacion-autocomplete'),
        label="Ubicación dentro del museo",
        empty_label='DESCONOCIDA',
        required=False
    )

    yacimiento = forms.ModelChoiceField(
        queryset=Yacimiento.objects.all(),
        widget=ModelSelect2WithPop(url='yacimiento-autocomplete'),
        label="Yacimiento de arqueología",
        empty_label='DESCONOCIDO',
        required=False
    )

    descripcion = forms.CharField(
        widget=Textarea(attrs={'cols': 80, 'rows': 2}),
        label="Descripción",
        required=False
    )
    
    class Meta:
      model = Arqueologia
      
      widgets = {
            'seccion': ModelSelect2WithPop(url='seccion-autocomplete'),
            'cultura': ModelSelect2WithPop(url='cultura-autocomplete'),
            'serie': ModelSelect2WithPop(url='serie-autocomplete'),
            'edad': ModelSelect2WithPop(url='edad-autocomplete'),
            'observaciones': Textarea(attrs={'cols': 80, 'rows': 2}),
            'hallazgos': Textarea(attrs={'cols': 80, 'rows': 2}),
            'fechaingreso': AdminDateWidget()
            #'bibliografia': FilteredSelectMultipleWithPop("Bibliografías", is_stacked=False, attrs={'cols': 80, 'rows': 20}),
            #'material': FilteredSelectMultipleWithPop("Materiales", is_stacked=False, attrs={'cols': 80, 'rows': 20}),
      }
      
      fields = "__all__"
      
      class Media:
           css = {'all': ('/static/admin/css/widgets.css',),}
           js = ('/admin/jsi18n',)
      

class BibliografiaForm(forms.ModelForm):    
    class Meta:
       model = Bibliografia
       widgets = {
            #'escritor': SelectWithPop(attrs={'cols': 80, 'rows': 30}),
            'escritor': ModelSelect2WithPop(url='escritor-autocomplete'),
            }
       fields = "__all__"

class MovimientoForm(forms.ModelForm):
    class Meta:
       model = Movimiento
       fields = "__all__"

class EstudioForm(forms.ModelForm):
    class Meta:
       model = Estudio
       fields = "__all__"
       
class MaterialForm(forms.ModelForm):
    class Meta:
       model = Material
       fields = "__all__"

       
class PaisForm(forms.ModelForm):
    class Meta:
       model = Pais
       fields = "__all__"
       
class SeccionForm(forms.ModelForm):
    class Meta:
       model = Seccion
       fields = "__all__"

class SerieForm(forms.ModelForm):
    class Meta:
       model = Serie
       fields = "__all__"

class CulturaForm(forms.ModelForm):
    class Meta:
       model = Cultura
       fields = "__all__"   

class EdadForm(forms.ModelForm):
    class Meta:
       model = Edad
       fields = "__all__"       

class YacimientoForm(forms.ModelForm):
    class Meta:
       model = Yacimiento
       widgets = {
            'municipio': autocomplete.ModelSelect2(url='municipio-autocomplete'),
            }
       fields = "__all__"
       exclude = ['lat','lng']

class MapaForm(forms.ModelForm):
    class Meta:
       model = Yacimiento
       widgets = {
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput()
            }
       fields = ['lat','lng']

class UbicacionForm(forms.ModelForm):
    class Meta:
       model = Ubicacion
       fields = "__all__"


class BellasArtesForm(forms.ModelForm):
    bibliografia = forms.ModelMultipleChoiceField(
        queryset=Bibliografia.objects.all(),
        widget=ModelSelect2MultipleWithPop(url='bibliografia-autocomplete'),
        label="Bibliografía",
        required=False
    )

    tecnica = forms.ModelMultipleChoiceField(
        queryset=Tecnica.objects.all(),
        widget=ModelSelect2MultipleWithPop(url='tecnica-autocomplete'),
        label="Técnicas",
        required=False
    )

    iconografia = forms.ModelMultipleChoiceField(
        queryset=Iconografia.objects.all(),
        widget=ModelSelect2MultipleWithPop(url='iconografia-autocomplete'),
        label="Iconografías",
        required=False
    )
    
    ubicacion = forms.ModelChoiceField(
        queryset=Ubicacion.objects.all(),
        widget=ModelSelect2WithPop(url='ubicacion-autocomplete'),
        label="Ubicación dentro del museo",
        empty_label='DESCONOCIDA',
        required=False
    )

    descripcion = forms.CharField(
        widget=Textarea(attrs={'cols': 80, 'rows': 2}),
        label="Descripción",
        required=False
    )
    
    class Meta:
       model = Bellasartes
       widgets = {
            #'bibliografia': FilteredSelectMultipleWithPop("Bibliografías", is_stacked=False, attrs={'cols': 80, 'rows': 20}),
            #'tecnica': FilteredSelectMultipleWithPop("Técnicas", is_stacked=False, attrs={'cols': 80, 'rows': 20}),
            #'iconografia': FilteredSelectMultipleWithPop("Iconografias", is_stacked=False, attrs={'cols': 80, 'rows': 20}),
            'autor': ModelSelect2WithPop(url='autor-autocomplete'),
            'soporte': ModelSelect2WithPop(url='soporte-autocomplete'),
            'movimientos': MultipleSelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'donante': ModelSelect2WithPop(url='donante-autocomplete'),
            'contexto': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'produ': ModelSelect2WithPop(url='pais-autocomplete'),
            'procedencia': ModelSelect2WithPop(url='yacimiento-autocomplete'),
            'estilo': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'observaciones': Textarea(attrs={'cols': 80, 'rows': 2}),
            'fechaingreso': AdminDateWidget()
        }
       fields = "__all__"
       exclude = ['objetos_relacionados','produ']

       class Media:
            css = {'all': ('/static/admin/css/widgets.css',),}
            js = ('/admin/jsi18n',)

class AutorForm(forms.ModelForm):
    class Meta:
       model = Autor
       fields = "__all__"

class SoporteForm(forms.ModelForm):
    class Meta:
       model = Soporte
       fields = "__all__"

class TecnicaForm(forms.ModelForm):
    class Meta:
       model = Tecnica
       fields = "__all__"

class EstudioForm(forms.ModelForm):
    class Meta:
       model = Estudio
       fields = "__all__"

class DonanteForm(forms.ModelForm):
    class Meta:
       model = Donante
       fields = "__all__"


class InformeEstadoForm(forms.ModelForm):
   objeto = forms.ModelChoiceField(queryset=Objeto.objects.all(),widget=forms.HiddenInput(attrs={'readonly':'readonly'})) #no se permite editar el id del objeto que va ligado a un informe de estado
   fecha = forms.DateField(widget=AdminDateWidget)
   estudio = forms.ModelMultipleChoiceField(
        queryset=Estudio.objects.all(),
        widget=ModelSelect2MultipleWithPop(url='estudio-autocomplete'),
        label="Estudios realizados ",
        required=False
    )

   class Meta:
       model = InformeEstado
       widgets = {
            'objetivo': Textarea(attrs={'cols': 80, 'rows': 2}),
            'observaciones': Textarea(attrs={'cols': 80, 'rows': 2}),
            'marco': Textarea(attrs={'cols': 80, 'rows': 2}),
            'obra': Textarea(attrs={'cols': 80, 'rows': 2}),
            'propuesta': Textarea(attrs={'cols': 80, 'rows': 2})
            }
       fields = "__all__"
       

class InformeArqueoForm(forms.ModelForm):
  objeto = forms.ModelChoiceField(queryset=Objeto.objects.all(),widget=forms.HiddenInput(attrs={'readonly':'readonly'}))
  fecha = forms.DateField(widget=AdminDateWidget)
  
  class Meta:
      model = InformeArqueo
      widgets = {
            'diagnostico': Textarea(attrs={'cols': 80, 'rows': 2}),
            'proyecto': Textarea(attrs={'cols': 80, 'rows': 2}),
            'desarrollo': Textarea(attrs={'cols': 80, 'rows': 2})
            }
      fields = "__all__"

class EscritorForm(forms.ModelForm):
    class Meta:
       model = Escritor
       fields = "__all__"
       
class IntervencionForm(forms.ModelForm):
    estado_rel = forms.ModelChoiceField(queryset=InformeEstado.objects.all(),widget=forms.HiddenInput(attrs={'readonly':'readonly'})) #no se permite editar el estado que va ligado a un informe de intervención
    fecha = forms.DateField(widget=AdminDateWidget)
    
    class Meta:
       model = InformeIntervencion
       widgets = {
            'justificacion': Textarea(attrs={'cols': 80, 'rows': 2}),
            'criterios': Textarea(attrs={'cols': 80, 'rows': 2}),
            'descripcioninter': Textarea(attrs={'cols': 80, 'rows': 2}),
            'recom': Textarea(attrs={'cols': 80, 'rows': 2})
            }
       fields = "__all__"

class IconografiaForm(forms.ModelForm):
    class Meta:
       model = Iconografia
       fields = "__all__"
    
class ExposicionForm(forms.ModelForm):
    class Meta:
       model = Exposicion
       fields = "__all__"

class MovimientoForm(forms.ModelForm):
    class Meta:
       model = Movimiento
       fields = "__all__"

class ExtractoForm(forms.ModelForm):
  bibliografia = forms.ModelChoiceField(queryset=Bibliografia.objects.all(),widget=forms.HiddenInput(attrs={'readonly':'readonly'}))
  objeto = forms.ModelChoiceField(queryset=Objeto.objects.all(),widget=forms.HiddenInput(attrs={'readonly':'readonly'}))
  class Meta:
      model = Biblio_Objeto
      widgets = {
            'extracto': Textarea(attrs={'cols': 80, 'rows': 2})
            }
      fields = "__all__"
