#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from .views import *
from django.contrib.auth import views
from .forms import LoginForm
from .forms import *

urlpatterns = [
    url(r'^$',index, name='index'),
    url(r'^error',error, name='error'),
    url(r'^accounts/login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^accounts/logout/$', views.logout, {'next_page': 'login'}),
    #VISTA DEL SUPER FORMULARIO DE ARQUEOLOGIA
    url(r'^registrararqueologia', arqueologia_crear , name='registrararqueologia'),
    url(r'^registrarbellasartes', bellasartes_crear , name='registrarbellasartes'),
    url(r'^anadir_prestamo', movimiento_crear , name='crearmovimiento'),
    url(r'^verarqueologia', arqueologia_lista , name='verarqueologia'),
    url(r'^verbellasartes', bellasartes_lista , name='verbellasartes'),
    url(r'^arqueologia/(?P<pk>\d+)/$', arqueologia_detalle, name='detallearqueo'),
    url(r'^bellasartes/(?P<pk>\d+)/$', bellasartes_detalle, name='detallebellasartes'),    
    url(r'^arqueologia/(?P<pk>\d+)/editar/$', arqueologia_actualizar, name='actualizararqueologia'),
    url(r'^bellasartes/(?P<pk>\d+)/editar/$', bellasartes_actualizar, name='actualizarbellasartes'),
    url(r'^arqueologia/(?P<pk>\d+)/borrar/$', arqueologia_borrar, name='borrararqueologia'),
    url(r'^bellasartes/(?P<pk>\d+)/borrar/$', bellasartes_borrar, name='borrarbellasartes'),
    url(r'^autor/(?P<pk>\d+)/actualizar/$', autor_actualizar, name='actualizarautor'),
    #EDICIÓN DE CAMPOS DE BA
    url(r'^iconografia/(?P<pk>\d+)/actualizar/$', iconografia_actualizar, name='actualizaricon'),
    url(r'^soporte/(?P<pk>\d+)/actualizar/$', soporte_actualizar, name='actualizarsoporte'),
    url(r'^tecnica/(?P<pk>\d+)/actualizar/$', tecnica_actualizar, name='actualizartecnica'),
    url(r'^ubicacion/(?P<pk>\d+)/actualizar/$', ubicacion_actualizar, name='actualizarubicacion'),
    url(r'^bibliografia/(?P<pk>\d+)/actualizar/$', bibliografia_actualizar, name='actualizarbibliografia'),
    url(r'^material/(?P<pk>\d+)/actualizar/$', material_actualizar, name='actualizarmaterial'),
    #EDICIÓN DE CAMPOS DE ARQUEO
    url(r'^edad/(?P<pk>\d+)/actualizar/$', edad_actualizar, name='actualizaredad'),
    url(r'^cultura/(?P<pk>\d+)/actualizar/$', cultura_actualizar, name='actualizarcultura'),
    url(r'^yacimiento/(?P<pk>\d+)/actualizar/$', yacimiento_actualizar, name='actualizaryacimiento'),
    #VISTAS PARA AGREGAR ELEMENTOS EXTERNOS DE LA TABLA OBJETO
    url(r'^agregar/bibliografia/',newBibliografia, name='nuevabibliografia'),
    url(r'^agregar/movimientos/', newMovimiento, name='nuevo-movimiento'),
    url(r'^agregar/estudio/' ,newEstudio, name='nuevoestudio'),
    url(r'^agregar/ubicacion/' ,newUbicacion, name='nuevoubicacion'),
    #VISTAS PARA AGREGAR ELEMENTOS DE TABLAS EXTERNAS DE ARQUEOLOGIA
    url(r'^agregar/material/',newMaterial, name='nuevomaterial'),
    url(r'^agregar/cultura/',newCultura, name='nuevacultura'),
    url(r'^agregar/seccion/',newSeccion, name='nuevaseccion'),
    url(r'^agregar/produ/',newPais, name='nuevopais'),
    url(r'^agregar/serie/',newSerie, name='nuevaserie'),
    url(r'^agregar/escritor/',newEscritor, name='nuevoescritor'),
    url(r'^agregar/procedencia/',newYacimiento, name='nuevaprocedencia'),
    url(r'^agregar/yacimiento/',newYacimiento, name='nuevoyacimiento'),
    #VISTAS PARA AGREGAR ELEMENTOS EXTERNOS DE BA
    url(r'^agregar/donante/',newDonante, name='nuevodonante'),
    url(r'^agregar/tecnica/',newTecnica, name='nuevotecnica'),
    url(r'^agregar/soporte/',newSoporte, name='nuevosoporte'),
    url(r'^agregar/autor/',newAutor, name='nuevoautor'),
    url(r'^agregar/iconografia/',newIconografia, name='nuevoiconografia'),
    #BUSQUEDAS
    url(r'^search-arqueologia/$',searcharqueologia, name='search-arqueologia'),
    url(r'^search-bellasartes/$',searchbellasartes, name='search-bellasartes'),
    #LISTADO DE INFORMES DE ESTADO
    url(r'^registrarestado/(?P<pk>\d+)/$', estado_crear , name='registrarestado'),
    url(r'^registrarintervencion/(?P<pk>\d+)/$', intervencion_crear , name='registrarintervencion'),
    url(r'^estado/(?P<pk>\d+)/$', estado_detalle, name='detalleestado'),
    url(r'^estadoactualizar/(?P<pk>\d+)/$', estado_actualizar, name='actuestado'),
    url(r'^autor_clasificacion/(?P<pk>\d+)/$', autores_clasi, name='autores-clasificacion'),
    url(r'^verautores', autores_lista, name='autores-listado'),
    url(r'^informearqueo_crear/(?P<pk>\d+)/$', informearqueo_crear,name='informe-arqueo-crear'),
    url(r'^informearqueo_ver/(?P<pk>\d+)/$', informearqueo_detalle,name='informe-arqueo-ver'),
    url(r'^informearqueo_actu/(?P<pk>\d+)/$', informearqueo_actualizar,name='informe-arqueo-actu'),
]



handler404 = handler404
handler500 = handler500
