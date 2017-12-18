#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from .views import *
from django.contrib.auth import views
from .forms import LoginForm
from .forms import *
from django.views.i18n import javascript_catalog
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$',index, name='index'),
    url(r'^index$',index, name='index'),
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
    url(r'^escritor/(?P<pk>\d+)/actualizar/$', escritor_actualizar, name='actualizarescritor'),
    #EDICIÓN DE CAMPOS DE BA
    url(r'^iconografia/(?P<pk>\d+)/actualizar/$', iconografia_actualizar, name='actualizaricon'),
    url(r'^soporte/(?P<pk>\d+)/actualizar/$', soporte_actualizar, name='actualizarsoporte'),
    url(r'^tecnica/(?P<pk>\d+)/actualizar/$', tecnica_actualizar, name='actualizartecnica'),
    url(r'^estudio/(?P<pk>\d+)/actualizar/$', estudio_actualizar, name='actualizarestudio'),
    url(r'^ubicacion/(?P<pk>\d+)/actualizar/$', ubicacion_actualizar, name='actualizarubicacion'),
    url(r'^bibliografia/(?P<pk>\d+)/actualizar/$', bibliografia_actualizar, name='actualizarbibliografia'),
    url(r'^material/(?P<pk>\d+)/actualizar/$', material_actualizar, name='actualizarmaterial'),
    #EDICIÓN DE CAMPOS DE ARQUEO
    url(r'^edad/(?P<pk>\d+)/actualizar/$', edad_actualizar, name='actualizaredad'),
    url(r'^cultura/(?P<pk>\d+)/actualizar/$', cultura_actualizar, name='actualizarcultura'),
    url(r'^yacimiento/(?P<pk>\d+)/actualizar/$', yacimiento_actualizar, name='actualizaryacimiento'),
    url(r'^extracto/(?P<pk_biblio>\d+)-(?P<pk_objeto>\d+)/actualizar/$', extracto_actualizar, name='actualizarextracto'),
    #VISTAS PARA AGREGAR ELEMENTOS EXTERNOS DE LA TABLA OBJETO
    url(r'^agregar/bibliografia/',newBibliografia, name='nuevabibliografia'),
    url(r'^agregar/movimientos/', newMovimiento, name='nuevo-movimiento'),
    url(r'^agregar/estudio/' ,newEstudio, name='nuevoestudio'),
    url(r'^agregar/ubicacion/' ,newUbicacion, name='nuevoubicacion'),
    #VISTAS PARA AGREGAR ELEMENTOS DE TABLAS EXTERNAS DE ARQUEOLOGIA
    url(r'^agregar/material/',newMaterial, name='nuevomaterial'),
    url(r'^agregar/cultura/',newCultura, name='nuevacultura'),
    url(r'^agregar/edad/',newEdad, name='nuevaedad'),
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
    url(r'^agregar/biblio_objeto/(?P<clase>\w+)/(?P<pk_biblio>\d+)-(?P<pk_objeto>\d+)',extracto_crear, name='nuevoextracto'),
    #BUSQUEDAS
    url(r'^search-arqueologia/$',searcharqueologia, name='search-arqueologia'),
    url(r'^search-bellasartes/$',searchbellasartes, name='search-bellasartes'),
    #LISTADO DE INFORMES DE ESTADO
    url(r'^registrarestado/(?P<pk>\d+)/$', estado_crear , name='registrarestado'),
    url(r'^registrarintervencion/(?P<pk>\d+)/$', intervencion_crear , name='registrarintervencion'),
    url(r'^estado/(?P<pk>\d+)/$', estado_detalle, name='detalleestado'),
    url(r'^estadoactualizar/(?P<pk>\d+)/$', estado_actualizar, name='actuestado'),
    url(r'^interactualizar/(?P<pk>\d+)/$', inter_actualizar, name='actuinter'),
    url(r'^autor_clasificacion/(?P<pk>\d+)/$', autores_clasi, name='autores-clasificacion'),
    url(r'^verautores', autores_lista, name='autores-listado'),
    url(r'^informearqueo_crear/(?P<pk>\d+)/$', informearqueo_crear,name='informe-arqueo-crear'),
    url(r'^informearqueo_ver/(?P<pk>\d+)/$', informearqueo_detalle,name='informe-arqueo-ver'),
    url(r'^informearqueo_actu/(?P<pk>\d+)/$', informearqueo_actualizar,name='informe-arqueo-actu'),
    #OTROS LISTADOS
    url(r'^verbiblio', biblio_lista, name='biblio-listado'),
    url(r'^vercultura', cultura_lista, name='cultura-listado'),
    url(r'^verescritor', escritor_lista, name='escritor-listado'),
    url(r'^vericono', icono_lista, name='icono-listado'),
    url(r'^vermaterial', material_lista, name='material-listado'),
    url(r'^versoporte', soporte_lista, name='soporte-listado'),
    url(r'^vertecnica', tecnica_lista, name='tecnica-listado'),
    url(r'^veryacimiento', yacimiento_lista, name='yacimiento-listado'),
    url(r'^verextracto', extracto_lista, name='extracto-listado'),
    url(r'^verestudio', estudio_lista, name='estudio-listado'),
    #OTROS INDICES
    url(r'^index=ba', index_ba, name='index-ba'),
    url(r'^index=arq', index_arq, name='index-arq'),
    url(r'^index=docu', index_docu, name='index-docu'),
    #AÑADIR LOACLIZACIÓN (GOOGLE MAPS)
    url(r'^yacimiento/(?P<pk>\d+)/mapa/$', yacimiento_mapa, name='mapayacimiento'),
    #EXPORTAR A CSV
    url(r'^informearqueo_csv/(?P<year>\d{4})/$', informearqueo_csv, name='informe-arqueo-csv'),
    url(r'^informeba_csv/(?P<year>\d{4})/$', informeba_csv, name='informe-ba-csv'),
    #JAVASCRIPT FOR ADMIN
    url(r'^admin/jsi18n/$', javascript_catalog, name='admin-js'),
    #INCIDENCIAS ( GLPI )
    url(r'^ticket/crear_ticket/$', RedirectView.as_view(url='http://glpi.dca.ccul.junta-andalucia.es/', permanent=False), name='incidencias'),
    #FILTROS AUTOCOMPLETE
    url(r'^arqueologia-autocomplete/$',ArqueologiaAutocomplete.as_view(),name='arqueologia-autocomplete',),
    url(r'^seccion-autocomplete/$',SeccionAutocomplete.as_view(),name='seccion-autocomplete',),
    url(r'^cultura-autocomplete/$',CulturaAutocomplete.as_view(),name='cultura-autocomplete',),
    url(r'^serie-autocomplete/$',SerieAutocomplete.as_view(),name='serie-autocomplete',),
    url(r'^yacimiento-autocomplete/$',YacimientoAutocomplete.as_view(),name='yacimiento-autocomplete',),
    url(r'^edad-autocomplete/$',EdadAutocomplete.as_view(),name='edad-autocomplete',),
    url(r'^soporte-autocomplete/$',SoporteAutocomplete.as_view(),name='soporte-autocomplete',),
    url(r'^pais-autocomplete/$',PaisAutocomplete.as_view(),name='pais-autocomplete',),
    url(r'^autor-autocomplete/$',AutorAutocomplete.as_view(),name='autor-autocomplete',),
    url(r'^donante-autocomplete/$',DonanteAutocomplete.as_view(),name='donante-autocomplete',),
    url(r'^ubicacion-autocomplete/$',UbicacionAutocomplete.as_view(),name='ubicacion-autocomplete',),
    url(r'^material-autocomplete/$',MaterialAutocomplete.as_view(),name='material-autocomplete',),
    url(r'^bibliografia-autocomplete/$',BibliografiaAutocomplete.as_view(),name='bibliografia-autocomplete',),
    url(r'^tecnica-autocomplete/$',TecnicaAutocomplete.as_view(),name='tecnica-autocomplete',),
    url(r'^iconografia-autocomplete/$',IconografiaAutocomplete.as_view(),name='iconografia-autocomplete',),
    url(r'^escritor-autocomplete/$',EscritorAutocomplete.as_view(),name='escritor-autocomplete',),
    url(r'^municipio-autocomplete/$',MunicipioAutocomplete.as_view(),name='municipio-autocomplete',),
    url(r'^estudio-autocomplete/$',EstudioAutocomplete.as_view(),name='estudio-autocomplete',)
]



handler404 = handler404
handler500 = handler500
