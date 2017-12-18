#!/usr/bin/env python
# -*- coding: utf-8 -*
from __future__ import unicode_literals
from django.utils.encoding import smart_unicode, uri_to_iri, iri_to_uri
from django.db import models
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from datetime import datetime, date
from uuid import uuid4
from PIL import Image
import os.path
import xml.etree.cElementTree as et

##################################
#       Ponerle el nombre del
#       objeto a la foto
################################

def wrapper():
    return

def path_and_rename(path):
  def wrapper(instance, filename):
    upload_to = os.path.join('objetos',path)
    ext = filename.split('.')[-1].lower()
    # get filename
    name = instance.numinv.replace("/","_")
    filename = '{}.{}'.format(name, ext)
    # return the whole path to the file
    return uri_to_iri(os.path.join(upload_to, filename))
  return wrapper
    
def resize_image(foto):
  max_size = 360
  image = Image.open(foto)
  (width, height) = image.size
  if width > max_size or height > max_size:
    if width > height:
      factor = float(width) / float(max_size)
    else:
      factor = float(height) / float(max_size)
    size = ( int(width/factor), int(height/factor) )
    image = image.resize(size, Image.ANTIALIAS)
  image.save(foto.path)

def validate_svg(f):
  if not is_svg(f):
    raise ValidationError("Este fichero no esta en formato svg")

def is_svg(f):
  return f.name.split('.')[-1].lower() == "svg"
  # LA VALIDACION INFERIOR NO FUNCIONA ( TO DO )
  f.open(mode='rb')
  f.seek(0)
  tag = None
  try:
    for event, el in et.iterparse(f, ('start',)):
      tag = el.tag
      break
  except et.ParseError:
    pass
  return tag == '{http://www.w3.org/2000/svg}svg'

########################################
# Datos comunes a la clase padre Objeto
########################################

class Escritor(models.Model):
    nombre =  models.CharField(max_length=60)
    apellidos = models.CharField(max_length=90)
    
    def __str__(self):
      return smart_unicode(self.nombre) + " " + smart_unicode(self.apellidos)
    def __unicode__(self):
      return unicode(self.nombre) + unicode(" ") + unicode(self.apellidos)
      return unicode(self.nombre) + unicode(" ") + unicode(self.apellidos)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Escritores"
        unique_together = ('nombre', 'apellidos')

class Bibliografia(models.Model):
    escritor = models.ForeignKey(Escritor,verbose_name="Escritor ")
    titulo = models.CharField(max_length=60,verbose_name="Obra que hace referencia ")
    edicion = models.CharField(max_length=10,verbose_name="Edición",blank=True,null=True)
    
    def __str__(self):
      return smart_unicode(self.titulo) + " ( " + smart_unicode(self.escritor.nombre) + " " + smart_unicode(self.escritor.apellidos) +  " )"
    def __unicode__(self):
      return self.titulo + unicode(" ( ") + self.escritor.nombre + unicode(" ") + self.escritor.apellidos +  unicode(" )")

    class Meta:
        ordering = ["edicion"]
        unique_together = ('titulo', 'escritor')
        verbose_name_plural = "Bibliografias"


class Continente(models.Model):
    nombre = models.CharField(max_length=40)
    def __str__(self):
        return smart_unicode(self.nombre)
    def __unicode__(self):
        return self.nombre
        
class Pais(models.Model):
    continente = models.ForeignKey(Continente)
    nombre = models.CharField(max_length=40)
    def __str__(self):
        return smart_unicode(self.nombre)
    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ["nombre"]
        unique_together = ('nombre', 'continente')
        verbose_name_plural = "Paises"
        
class Ca(models.Model):
    nombre = models.CharField(max_length=20)
    pais = models.ForeignKey(Pais)
    def __str__(self):
        return smart_unicode(self.nombre)
    def __unicode__(self):
        return self.nombre
        
    class Meta:
        ordering = ["nombre"]
        unique_together = ('nombre', 'pais')
        verbose_name_plural = "Comunidades autónomas"
 
#En España, un municipio es, según la Ley reguladora de las Bases del Régimen Local, la entidad local básica de la organización territorial del Estado.            
# municipio pertenece a provincia que pertenece a comunidad autonoma en ESPAÑA

class Provincia(models.Model):
    ca = models.ForeignKey(Ca)
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return smart_unicode(self.nombre)
    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ["nombre"]
        unique_together = ('nombre', 'ca')
        verbose_name_plural = "Provincias"
        
class Municipio(models.Model):
    provincia = models.ForeignKey(Provincia)
    nombre = models.CharField(max_length=40)
    def __str__(self):
        return smart_unicode(self.nombre)
    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ["nombre"]
        unique_together = ('nombre', 'provincia')
        verbose_name_plural = "Municipios"
        
class Estudio(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return smart_unicode(self.nombre)
    def __unicode__(self):
        return unicode(self.nombre)


class Ubicacion(models.Model):
    tipo_selec = (('SALA','SALA'),
                  ('PEINE','PEINE'),
                  ('ALMACEN','ALMACÉN'),
                  )
    tipo = models.CharField(choices = tipo_selec,max_length=10,verbose_name="Tipo",blank=False,null=False)   
    nombre = models.CharField(max_length=20)
    
    def __str__(self):
        return smart_unicode(self.tipo) + " " + smart_unicode(self.nombre)
    def __unicode__(self):
        return self.tipo + unicode(" ") + self.nombre
        
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Ubicaciones del Museo"
        

########################################
# Datos clase padre Objeto
########################################

class Objeto(models.Model):
    anverso = models.ImageField(upload_to=path_and_rename('anversos'),blank=True,null=True)
    reverso = models.ImageField(upload_to=path_and_rename('reversos'),blank=True,null=True)
    codigo_selec = (('DJ', 'DJ'),
               ('CE', 'CE'),
               ('DO', 'DO'),
               ('DE', 'DE'),
               )
    codigo = models.CharField(choices = codigo_selec, max_length=2,verbose_name="Código",blank=True,null=True)
    ni_regex = RegexValidator(regex=r'^[0-9]+(/[a-zA-Z]+)?$',message='Formato no válido.\nUse: <digito(s)>[/<letra(s)>]')
    numinv = models.CharField(unique=True,max_length=10,validators=[ni_regex],verbose_name="Número de inventario ")  # Field name made lowercase.
    altura = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Altura en cm",blank=True,null=True)
    ancho = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Ancho en cm",blank=True,null=True)
    datacion = models.CharField(max_length=30,default='DESCONOCIDA',verbose_name="Cronología",blank=True,null=True)
    bibliografia = models.ManyToManyField(Bibliografia,blank=True)
    fechaingreso = models.CharField(max_length=50,verbose_name="Fecha de ingreso",default=date.today,blank=True,null=True)
    numero_entrada = models.IntegerField(verbose_name="Número de entrada",blank=True,null=True)
    ubicacion = models.ForeignKey(Ubicacion, models.SET_NULL, verbose_name ="Ubicación dentro del museo",blank=True,null=True)
    descripcion = models.TextField(blank=True,null=True,default=None)
    observaciones = models.TextField(blank=True,null=True)
    objetos_relacionados = models.ManyToManyField("self", models.SET_NULL, blank=True)

    def save(self):
      super(Objeto, self).save()
      if self.anverso:
        resize_image(self.anverso)
      if self.reverso:
        resize_image(self.reverso)

    def __str__(self):
      return smart_unicode(self.id)
    #def __unicode__(self):
      #return self.id
      
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Inventario general"  
      
########################################
#Campos especificos de arqueologia
########################################

class Museo(models.Model):
    nombre = models.CharField(max_length=30,verbose_name="Museo")
    ciudad = models.ForeignKey(Municipio)

    def __str__(self):
       return smart_unicode(self.nombre) 
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Museos"

class Exposicion(models.Model):
    nombre = models.CharField(max_length=30,verbose_name="Exposicion")
    museo = models.ForeignKey(Museo)

    def __str__(self):
        return smart_unicode(self.nombre) 
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Exposiciones"


class Serie(models.Model):
    nombre =  models.CharField(max_length=40)

    def __str__(self):
        return smart_unicode(self.nombre)
    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Series"


class Material(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return smart_unicode(self.nombre)
    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Materiales"
            
class Seccion (models.Model):
    nombre = models.CharField(max_length=30)
   
    def __str__(self):
	    return smart_unicode(self.nombre)
    def __unicode__(self):
	    return self.nombre
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Secciones de arqueologia"

class Cultura(models.Model):
    nombre = models.CharField(max_length=30)
    
    def __str__(self):
        return smart_unicode(self.nombre)
    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Culturas"
        
class Edad(models.Model):
    nombre = models.CharField(max_length=30)
    
    def __str__(self):
        return smart_unicode(self.nombre)
    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Edades"

#Fondos.Arqueologia.numinv: (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
#       HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.
#Fondos.Bellasartes.numinv: (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
#        HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.

class Yacimiento(models.Model):
    yacimiento = models.CharField(max_length=100,verbose_name="Nombre ")
    municipio =  models.ForeignKey(Municipio, models.SET_NULL, blank=True, null=True)
    lat = models.CharField(max_length=20, blank=True, null=True)
    lng = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        if self.municipio:
            return smart_unicode(self.yacimiento) + ". " +  smart_unicode(self.municipio)
        else:
            return smart_unicode(self.yacimiento) + ". SIN MUNICIPIO"
    def __unicode__(self):
        if self.municipio:
            return unicode(self.yacimiento) + unicode(". ") + unicode(self.municipio)
        else:
            return unicode(self.yacimiento) + unicode(". SIN MUNICIPIO")
    class Meta:
        ordering = ["yacimiento"]
        unique_together = ('yacimiento', 'municipio')
        verbose_name_plural = "Yacimientos de arqueologia"

class Arqueologia(Objeto):
    nombre = models.CharField(max_length=50,blank=False,null=True,verbose_name="Nombre ")
    seccion = models.ForeignKey(Seccion,models.SET_NULL,blank=True,null=True,verbose_name="Sección")
    hallazgos = models.TextField(blank=True,null=True,default=None)
    depositado =  models.CharField(max_length=20,blank=True,null=True,verbose_name="Depositado por")
    cultura = models.ForeignKey(Cultura,models.SET_NULL,blank=True,null=True)
    serie = models.ForeignKey(Serie,models.SET_NULL,blank=True,null=True)
    conservacion_selec = (('1', 'BUENO'),
               ('2', 'REGULAR'),
               ('3', 'MALO'),
               )
    conservacion = models.CharField(choices = conservacion_selec,max_length=1,blank=True,null=True,verbose_name="Conservación") 
    yacimiento = models.ForeignKey(Yacimiento,models.SET_NULL,blank=True,null=True)
    edad = models.ForeignKey(Edad,models.SET_NULL,blank=True,null=True)
    material = models.ManyToManyField(Material,blank=True)
   
    def __str__(self):
       return smart_unicode(self.numinv) + " - " + smart_unicode(self.nombre)
    def __unicode__(self):
       return self.numinv + " - " + self.nombre
       
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Arqueologia"
    def get_absolute_url(self):
        return "/arqueologia/%i/" % self.pk

########################################
#Campos especificos de Bellas Artes
########################################

class Tecnica(models.Model):
    nombre = models.CharField(max_length=30)
    
    def __str__(self):
       return smart_unicode(self.nombre) 
    def __unicode__(self):
       return self.nombre
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Tipos de tecnicas"

class Soporte(models.Model):
    nombre = models.CharField(max_length=30)
 
    def __str__(self):
      return smart_unicode(self.nombre)
    def __unicode__(self):
      return unicode(self.nombre)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Tipos de soportes"


class Donante(models.Model):
    nombre = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)  
      
    def __str__(self):
	    return smart_unicode(self.nombre) +  " " + smart_unicode(self.apellidos)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Donantes"
        
class Iconografia(models.Model):
    nombre = models.CharField(max_length=80,verbose_name="Iconografia")
    
    def __str__(self):
	    return smart_unicode(self.nombre) 
    def __unicode__(self):
	    return self.nombre
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Iconografias"

class Autor(models.Model):
    foto = models.ImageField(upload_to='autores',blank=True,null=True)
    alias = models.CharField(max_length=30,blank=True,null=True)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=60,blank=True,null=True)
    procedencia = models.CharField(max_length=90,blank=True,null=True)
    fnac = models.CharField(max_length=50,blank=True,null=True,verbose_name="Fecha de nacimiento")
    fdef = models.CharField(max_length=50,blank=True,null=True,verbose_name="Fecha de defunción")

    def save(self):
      super(Autor, self).save()
      if not self.alias or self.alias == "":
        autor = Autor.objects.get(pk=self.pk)
        autor.alias = autor.nombre
        autor.save()

    def __str__(self):
       if self.apellidos:
          return smart_unicode(self.nombre) + " " + smart_unicode(self.apellidos) + " (" + smart_unicode(self.alias) + " )"
       else:
          return smart_unicode(self.nombre) + " (" + smart_unicode(self.alias) + " )"
    def __unicode__(self):
       if self.apellidos:
          return unicode(self.nombre) + unicode(" ") + unicode(self.apellidos) + unicode(" ( ") + unicode(self.alias) + unicode(" )")
       else:
          return unicode(self.nombre) + unicode(" ( ") + unicode(self.alias) + unicode(" )")
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Autores"
         
class Bellasartes(Objeto):
    titulo = models.CharField(max_length=150,verbose_name="Título ")
    iconografia = models.ManyToManyField(Iconografia,verbose_name="Iconografía",blank=True)
    produ = models.ForeignKey(Pais,verbose_name="Producido en",blank=True,null=True)
    soporte = models.ForeignKey(Soporte,models.SET_NULL,blank=True,null=True,verbose_name="Soporte pictórico")
    procedencia = models.ForeignKey(Yacimiento,blank=True,null=True)
    tecnica = models.ManyToManyField(Tecnica,verbose_name="Técnica",blank=True)
    adquirido_selec = (('COMPRA', 'COMPRA'),
               ('DEPOSITO', 'DEPOSITO'),
               ('DESAMORTIZACION', 'DESAMORTIZACIÓN'),
               ('DONACION', 'DONACIÓN'),
               ('LEGADO', 'LEGADO'),
               )
    autor = models.ForeignKey(Autor,models.SET_NULL,blank=True,null=True)
    formaingreso = models.CharField(choices = adquirido_selec,max_length=15,verbose_name="Forma de ingreso",blank=True,null=True)
    donante = models.ForeignKey(Donante,models.SET_NULL,blank=True,null=True)
    def __str__(self):
       return smart_unicode(self.numinv) + " - " + smart_unicode(self.titulo)
    def __unicode__(self):
       return self.numinv + " - " + self.titulo
    class Meta:
        ordering = ["titulo"]
        verbose_name_plural = "Bellas Artes"
    def get_absolute_url(self):
        return "/bellasartes/%i/" % self.pk


class InformeEstado(models.Model):
    objeto = models.ForeignKey(Objeto,verbose_name="Objeto sobre el que se realiza el informe")#id del objeto 
    nombre_res = models.CharField(max_length=30,verbose_name=("Nombre del Restaurador "))
    ape_res = models.CharField(max_length=50,verbose_name=("Apellidos del Restaurador "))
    fecha =  models.DateField(default=datetime.now,verbose_name=("Fecha del informe de estado"),blank=True,null=True)  
    objetivo = models.TextField(verbose_name=("Objetivo del informe "))
    estudio = models.ManyToManyField(Estudio, verbose_name="Estudios realizados ",blank=True)
    observaciones = models.TextField(verbose_name="Observaciones ")
    marco = models.TextField(verbose_name=("Marco "))
    obra = models.TextField(verbose_name=("Obra "))
    prioridad = models.IntegerField(verbose_name="Prioridad ",validators=[MinValueValidator(1),MaxValueValidator(6)]) #de menos a más
    propuesta = models.TextField(verbose_name=("Conclusiones y propuesta de intervención "))
    
    def __str__(self):
       return  " Prioridad:" + smart_unicode(self.prioridad)
           
    class Meta:
        ordering = ["fecha"]
        verbose_name_plural = "Estados" 
   
    def get_absolute_url(self):
        return "/estado/%i/" % self.pk

      
class InformeIntervencion(models.Model):
    estado_rel = models.OneToOneField(InformeEstado, primary_key=True)
    tipo = models.CharField(max_length=80,verbose_name="Tipo ")
    interventor = models.CharField(max_length=80,verbose_name="Restaurador ",blank=True,null=True)
    fecha =  models.DateField(default=datetime.now,verbose_name=("Fecha del informe de intervención"),blank=True,null=True)  
    justificacion = models.TextField(verbose_name="Justificación de la Intervención ")
    criterios = models.TextField(verbose_name="Criterios ")
    estudios = models.BooleanField(default=False,verbose_name="¿Estudios?")
    descripcioninter = models.TextField(verbose_name="Descripción ")
    recom = models.TextField(verbose_name="Conclusiones y recomendaciones ")
    priori_des = models.IntegerField(verbose_name="Prioridad tras Intervención ",validators=[MinValueValidator(1),MaxValueValidator(6)])
    svg1 = models.FileField(upload_to="objetos/svg",validators=[validate_svg],verbose_name="Gráfico svg de la zona intervenida",blank=True,null=True)
    svg2 = models.FileField(upload_to="objetos/svg",validators=[validate_svg],verbose_name="Gráfico svg de la zona intervenida",blank=True,null=True)
    svg3 = models.FileField(upload_to="objetos/svg",validators=[validate_svg],verbose_name="Gráfico svg de la zona intervenida",blank=True,null=True)
    
    def __str__(self):
        return smart_unicode(self.estado_rel) + smart_unicode(" → ") + smart_unicode(self.priori_des)
    def __unicode__(self):
        return unicode(self.estado_rel) + unicode(" → ") + unicode(self.priori_des)
    class Meta:
        ordering = ["fecha"]
        verbose_name_plural = "Intervenciones"

class InformeArqueo(models.Model):
    objeto = models.ForeignKey(Objeto,verbose_name="Objeto sobre el que se realiza el informe")
    nombre_res = models.CharField(max_length=30,verbose_name=("Nombre del Restaurador "))
    ape_res = models.CharField(max_length=50,verbose_name=("Apellidos del Restaurador ")) 
    diagnostico = models.TextField(verbose_name=("Diagnóstico "))
    proyecto = models.TextField(verbose_name=("Proyecto de intervención "))
    desarrollo = models.TextField(verbose_name=("Desarrollo "))
    fecha =  models.DateField(default=datetime.now,verbose_name=("Fecha del informe de conservación"),blank=True,null=True)  
    
    def __str__(self):
        return smart_unicode(self.id) 
    class Meta:
        ordering = ["fecha"]
        verbose_name_plural = "Intervenciones de arqueología"
    def get_absolute_url(self):
        return "/informearqueo_ver/%i/" % self.pk 

class Movimiento(models.Model): # Préstamos
    expo = models.ForeignKey(Exposicion)
    objeto = models.ForeignKey(Bellasartes)
    fecha_prestado = models.DateField(auto_now=False)
    fecha_devuelto = models.DateField(auto_now=False)
    
    def __str__(self):
      return smart_unicode(self.fecha_prestado) + " "  + smart_unicode(self.fecha_devuelto) + " " + smart_unicode(self.expo)
    class Meta:
        ordering = ["fecha_prestado"]
        verbose_name_plural = "Movimientos"

class Biblio_Objeto(models.Model):
    bibliografia = models.ForeignKey(Bibliografia,verbose_name="Bibliografía ")
    objeto = models.ForeignKey(Objeto,verbose_name="Objeto ")
    pagina = models.CharField(max_length=30,verbose_name="Página ")
    extracto = models.TextField(verbose_name="Extracto ")
    
    def __str__(self):
      return smart_unicode(self.id)

    class Meta:
        ordering = ["pagina"]
        verbose_name = "Extracto Bibliográfico"
        verbose_name_plural = "Extractos Bibliográficos"
