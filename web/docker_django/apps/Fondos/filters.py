# -*- coding: utf-8 -*-
import django_filters
from .models import *
from django import forms

#busqueda con los campos especificos en arqueologia
class ArqueologiaFilter(django_filters.FilterSet):
    depositado = django_filters.CharFilter(lookup_expr='icontains')
    numinv = django_filters.CharFilter(lookup_expr='icontains')
    material = django_filters.ModelMultipleChoiceFilter(queryset=Material.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Arqueologia
        fields = ['material', 'serie', 'seccion','cultura','edad','yacimiento','depositado']

#busqueda con los campos especificos de bellas artes
class BellasArtesFilter(django_filters.FilterSet):
    numinv = django_filters.CharFilter(lookup_expr='icontains')
    soporte = django_filters.ModelMultipleChoiceFilter(queryset=Soporte.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    titulo = django_filters.CharFilter(lookup_expr='icontains')
    tecnica = django_filters.ModelMultipleChoiceFilter(queryset= Tecnica.objects.all(),
        widget=forms.CheckboxSelectMultiple)
         
    class Meta:
        model = Bellasartes
        fields = ['numinv','tecnica', 'iconografia', 'titulo','autor','procedencia','donante']
