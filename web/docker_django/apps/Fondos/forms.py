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
from django import forms
from django.forms import extras

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
    class Meta:
      model = Arqueologia
      widgets = {
            'seccion': SelectWithPop(attrs={'cols': 80, 'rows': 30}),
            'ubicacion': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'bibliografia': MultipleSelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'serie': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'yacimiento': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'cultura': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'material': MultipleSelectWithPop(attrs={'cols': 80, 'rows': 20}),
        }
      fields = "__all__"
      

class BibliografiaForm(forms.ModelForm):
    class Meta:
       model = Bibliografia
       widgets = {
            'escritor': SelectWithPop(attrs={'cols': 80, 'rows': 30}),
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

class YacimientoForm(forms.ModelForm):
    class Meta:
       model = Yacimiento
       fields = "__all__"

class UbicacionForm(forms.ModelForm):
    class Meta:
       model = Ubicacion
       fields = "__all__"


class BellasArtesForm(forms.ModelForm):
   class Meta:
       model = Bellasartes
       widgets = {
            'ubicacion': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'bibliografia': MultipleSelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'tecnica': MultipleSelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'autor': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'soporte': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'movimientos': MultipleSelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'donante': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'contexto': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'produ': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'procedencia': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'estilo': SelectWithPop(attrs={'cols': 80, 'rows': 20}),
            'iconografia': MultipleSelectWithPop(attrs={'cols': 80, 'rows': 20}),
        }
       fields = "__all__"


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


class DonanteForm(forms.ModelForm):
    class Meta:
       model = Donante
       fields = "__all__"


class InformeEstadoForm(forms.ModelForm):
   objeto = forms.ModelChoiceField(queryset=Objeto.objects.all(),widget=forms.TextInput(attrs={'readonly':'readonly'})) #no se permite editar el id del objeto que va ligado a un informe de estado
   fecha = forms.DateField(widget=extras.SelectDateWidget)

   class Meta:
       model = InformeEstado
       widgets = {
            'estudio': MultipleSelectWithPop(attrs={'cols': 80, 'rows': 20})
            }
       fields = "__all__"

class InformeArqueoForm(forms.ModelForm):
  objeto = forms.ModelChoiceField(queryset=Objeto.objects.all(),widget=forms.TextInput(attrs={'readonly':'readonly'}))
  class Meta:
      model = InformeArqueo
      fields = "__all__"

class EscritorForm(forms.ModelForm):
    class Meta:
       model = Escritor
       fields = "__all__"
       
class IntervencionForm(forms.ModelForm):
    estado_rel = forms.ModelChoiceField(queryset=InformeEstado.objects.all(),widget=forms.TextInput(attrs={'readonly':'readonly'})) #no se permite editar el estado que va ligado a un informe de intervención
    class Meta:
       model = InformeIntervencion
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
