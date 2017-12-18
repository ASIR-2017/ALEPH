# -*- encoding: utf-8 -*
from django.contrib import admin
import decimal, csv
# Register your models here.
from .models import *
from django.http import HttpResponse

def exportar_arqueo(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Inventario_arqueología.csv"'
    writer = csv.writer(response)
    writer.writerow(['Código','Número de inventario', 'Nombre', 'Cultura', 'Edad', 'Yacimiento',])
    arqueo = queryset.values_list('codigo','numinv', 'nombre', 'cultura','edad')
    for arqueo in arqueo:
        writer.writerow(arqueo)
    return response
exportar_arqueo.short_description = 'Exportar a csv'

class AdminArqueologia(admin.ModelAdmin):
 list_display = ["nombre","seccion","serie","edad"]
 list_filter = ["seccion"]
 search_fields = ["numinv","nombre","seccion","serie","edad","material"]
 actions = [exportar_arqueo, ]
 class Meta:
     model = Arqueologia
     
     
class AdminArte(admin.ModelAdmin):
 list_display = ["numinv","titulo","autor","ubicacion","formaingreso"]
 list_display_links =["numinv"]
 list_filter = ["autor"]
 list_editable = ["titulo","ubicacion"]
 search_fields = ["numinv","titulo","autor","fechaingreso","ubicacion"]
 
        
 class Meta:
     model = Bellasartes
     
class AdminAutor(admin.ModelAdmin):
 list_display = ["nombre","apellidos","alias","fnac","fdef"]
 list_filter = ["nombre"]
 list_editable = ["apellidos","alias"]
 search_fields = ["nombre","alias","apellido"]
      
 class Meta:
     model = Autor 

class AdminBibliografia(admin.ModelAdmin):
 list_display = ["edicion"]
 search_fields = ["edicion"]
      
 class Meta:
     model = Bibliografia 


admin.site.register(Movimiento)
admin.site.register(Bibliografia,AdminBibliografia)
admin.site.register(Escritor)
admin.site.register(Serie)
admin.site.register(Seccion)
admin.site.register(Cultura)
admin.site.register(Edad)
admin.site.register(Arqueologia,AdminArqueologia)
admin.site.register(Tecnica)
admin.site.register(Soporte)
admin.site.register(Bellasartes,AdminArte)
admin.site.register(Donante)
admin.site.register(Material)
admin.site.register(Yacimiento)
admin.site.register(Objeto)
admin.site.register(Estudio)
admin.site.register(Continente)
admin.site.register(Pais)
admin.site.register(InformeEstado)
admin.site.register(InformeIntervencion)
admin.site.register(InformeArqueo)
admin.site.register(Iconografia)
admin.site.register(Ca)
admin.site.register(Ubicacion)
admin.site.register(Provincia)
admin.site.register(Municipio)
admin.site.register(Museo)
admin.site.register(Exposicion)
admin.site.register(Autor,AdminAutor)
admin.site.register(Biblio_Objeto)
