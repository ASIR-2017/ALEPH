#!/usr/bin/env python
# -*- coding: utf-8 -*
from __future__ import unicode_literals
from django.db import models
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
import os.path
from uuid import uuid4

##################################
#       Ponerle el nombre del
#       objeto a la foto
################################

def path_and_rename(instance, filename):
    upload_to = 'Miniaturas'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}_{}.{}'.format(instance.codigo,instance.numinv, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
    

########################################
# Datos comunes a la clase padre Objeto
########################################

class Escritor(models.Model):
    nombre =  models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    
    def __str__(self):
      return str(self.nombre)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Escritoris"

class Bibliografia(models.Model):
    escritor = models.ForeignKey(Escritor)
    titulo = models.CharField(max_length=60, verbose_name="Obra que hace referencia")
    pagina = models.CharField(max_length=30,verbose_name="Página")
    edicion = models.CharField(max_length=10,verbose_name="Edicion")
    extracto = models.TextField()
    
    def __str__(self):
      return str(self.titulo)

    class Meta:
        ordering = ["edicion"]
        verbose_name_plural = "Bibliografias"


class Continente(models.Model):
    nombre = models.CharField(max_length=40)
    def __str__(self):
        return str(self.nombre)
class Pais(models.Model):
    continente = models.ForeignKey(Continente)
    nombre = models.CharField(max_length=40)
    def __str__(self):
        return str(self.nombre)
        
class Ca(models.Model):
    nombre = models.CharField(max_length=20)
    pais = models.ForeignKey(Pais)
    def __str__(self):
        return str(self.nombre)
        
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Comunidades autónomas"
 
#En España, un municipio es, según la Ley reguladora de las Bases del Régimen Local, la entidad local básica de la organización territorial del Estado.            
# municipio pertenece a provincia que pertenece a comunidad autonoma en ESPAÑA

class Provincia(models.Model):
    ca = models.ForeignKey(Ca)
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return str(self.nombre)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Provincias"
        
class Municipio(models.Model):
    provincia = models.ForeignKey(Provincia)
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return str(self.nombre)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Municipio"
        
class Estudio(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return str(self.nombre)


class Ubicacion(models.Model):
    tipo_selec = (('Sala','Sala'),
                  ('Peine','Peine'),
                  ('Almacén','Almacén'),
                  )
    tipo = models.CharField(choices = tipo_selec,max_length=10,verbose_name="Tipo")   
    nombre = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.tipo) + " " + str(self.nombre) 
        
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Ubicaciones del Museo"
        

########################################
# Datos clase padre Objeto
########################################


class Objeto(models.Model):
    anverso = models.ImageField(upload_to=path_and_rename)
    reverso  = models.ImageField(upload_to=path_and_rename)
    codigo_selec = (('DJ', 'DJ'),
               ('CE', 'CE'),
               ('DO', 'DO'),
               ('DE', 'DE'),
               )
    codigo = models.CharField(choices = codigo_selec, max_length=2,default='DJ',verbose_name="Código")
    numinv = models.IntegerField(unique=True,default=1,verbose_name="Número de inventario")  # Field name made lowercase.
    altura = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Altura en cm")
    ancho = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Ancho en cm")
    datacion = models.CharField(max_length=30,default='Desconocida',verbose_name="Fecha de la que data el objeto")
    bibliografia = models.ManyToManyField(Bibliografia,blank=True)
    fechaingreso = models.DateField(auto_now=True)
    numero_entrada = models.IntegerField(verbose_name="Numero entrada")
    ubicacion = models.ForeignKey(Ubicacion, default='1',verbose_name ="Ubicación dentro del museo")
    descripcion = models.TextField()
    observaciones = models.TextField()

    def __str__(self):
      return str(self.id)
      
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
       return str(self.nombre) 
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Museos"

class Exposicion(models.Model):
    nombre = models.CharField(max_length=30,verbose_name="Exposicion")
    museo = models.ForeignKey(Museo)

    def __str__(self):
	    return str(self.nombre) 
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Exposiciones"


class Serie(models.Model):
    nombre =  models.CharField(max_length=40)

    def __str__(self):
	    return str(self.nombre)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Series"


class Material(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
	    return str(self.nombre)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Materiales"
            
class Seccion (models.Model):
    nombre = models.CharField(max_length=10)
   
    def __str__(self):
	    return str(self.nombre)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Secciones de arqueologia"

class Cultura(models.Model):
    nombre = models.CharField(max_length=30)
    
    def __str__(self):
	    return str(self.nombre)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Culturas"
        

#Fondos.Arqueologia.numinv: (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
#       HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.
#Fondos.Bellasartes.numinv: (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
#        HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.

class Yacimiento(models.Model):
    yacimiento = models.CharField(max_length=30)
    municipio =  models.ForeignKey(Municipio)
   
    def __str__(self):
	    return str(self.yacimiento) + " , " +  str(self.municipio)
    class Meta:
        ordering = ["yacimiento"]
        verbose_name_plural = "Yacimientos de arqueologia"

class Arqueologia(Objeto):
    nombre = models.CharField(max_length=30)
    seccion = models.ForeignKey(Seccion)
    hallazgos = models.TextField(blank=True)
    depositado =  models.CharField(max_length=20,null=False,verbose_name="Depositado por")
    cultura = models.ForeignKey(Cultura,models.SET_NULL,blank=True,null=True,)
    serie = models.ForeignKey(Serie)
    conservacion_selec = (('1', 'Bueno'),
               ('2', 'Regular'),
               ('3', 'Malo'),
               )
    conservacion = models.CharField(choices = conservacion_selec,max_length=1,default='1') 
    yacimiento = models.ForeignKey(Yacimiento)
    edad_selec = (('Edad de piedra', 'Edad de piedra'),
               ('Edad de bronce', 'Edad de bronce'),
               ('Edad de metal', 'Edad de metal'),
               ('Edad de hierro', 'Edad de hierro'),
               ('Edad moderna', 'Edad moderna'),
               ('Edad de piedra', 'Edad desconocida'),
               )
    edad = models.CharField(choices = edad_selec, default='Edad desconocida',max_length=17)
    material = models.ManyToManyField(Material)
   
    def __str__(self):
       return " Nombre:" + str(self.nombre) + " Sección:" + str(self.seccion) + " Edad:" + str(self.edad) + " Cultura:" + str(self.cultura)

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
	       return str(self.nombre) 
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Tipos de tecnicas"

class Soporte(models.Model):
    nombre = models.CharField(max_length=10)
 
    def __str__(self):
      return str(self.nombre)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Tipos de soportes"


class Donante(models.Model):
    nombre = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)  
      
    def __str__(self):
	    return str(self.nombre) +  " " + str(self.apellidos)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Donantes"
        
class Iconografia(models.Model):
    nombre = models.CharField(max_length=30,verbose_name="Iconografia")
    
    def __str__(self):
	    return str(self.nombre) 
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Iconografias"

class Autor(models.Model):
    foto = models.ImageField(upload_to='autores/',default='nofoto.png')
    alias = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    procedencia = models.ForeignKey(Pais)
    apellidos = models.CharField(max_length=60,default='Desconocida')
    fnac = models.CharField(max_length=14,default='Desconocida',verbose_name="Fecha de nacimiento")
    fdef = models.CharField(max_length=14,default='Desconocida',verbose_name="Fecha de defunción")

    def __str__(self):
	      return str(self.nombre) + " ," + str(self.alias)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Autores"
         
class Bellasartes(Objeto):
    titulo = models.CharField(max_length=100)
    iconografia = models.ManyToManyField(Iconografia)
    produ = models.ForeignKey(Pais,verbose_name="Producido en",blank=True)
    soporte = models.ForeignKey(Soporte,verbose_name="Soporte pictórico")
    procedencia = models.ForeignKey(Yacimiento,blank=True)
    tecnica = models.ManyToManyField(Tecnica)
    adquirido_selec = (('Compra', 'Compra'),
               ('Donacion', 'Donacion'),
               ('Legado', 'Legado'),
               )
    autor = models.ForeignKey(Autor,models.SET_NULL,blank=True,null=True,)
    formaingreso = models.CharField(choices = adquirido_selec,max_length=8,default='1',verbose_name="Forma de ingreso")
    donante = models.ForeignKey(Donante,models.SET_NULL,blank=True,null=True,)
    def __str__(self):
	       return str(self.codigo) + str(self.numinv) +  " " + str(self.titulo)
    class Meta:
        ordering = ["titulo"]
        verbose_name_plural = "Bellas Artes"
    def get_absolute_url(self):
        return "/bellasartes/%i/" % self.pk


class InformeEstado(models.Model):
    objeto = models.ForeignKey(Objeto,verbose_name="Objeto sobre el que se realiza el informe")#id del objeto 
    nombre_res = models.CharField(max_length=30,verbose_name=("Nombre restaurador"))
    ape_res = models.CharField(max_length=50,verbose_name=("Apellidos del restaurador"))
    fecha = models.DateField(auto_now=True,verbose_name=("Fecha del informe de estado"))#fecha cuando se realiza el informe
    cartela = models.TextField()
    marco = models.TextField()
    estudio = models.ManyToManyField(Estudio, verbose_name="Estudios realizados")
    obra = models.TextField()
    prioridad = models.IntegerField(verbose_name="Prioridad",validators=[MinValueValidator(1),MaxValueValidator(6)]) #de menos a más
    propuesta = models.TextField()
    
    def __str__(self):
       return  " Prioridad:" + str(self.prioridad)
           
    class Meta:
        ordering = ["fecha"]
        verbose_name_plural = "Estados" 
   
    def get_absolute_url(self):
        return "/estado/%i/" % self.pk

      
class InformeIntervencion(models.Model):
    estado_rel = models.OneToOneField(InformeEstado, primary_key=True)
    tipo = models.CharField(max_length=80)
    justificacion = models.TextField(verbose_name="Justificación de la intervencion")
    criterios = models.TextField()
    estudios = models.BooleanField(default=False)
    fecha =  models.DateField(auto_now=True,verbose_name=("Fecha del informe de estado"))
    descripcioninter = models.TextField(verbose_name="Descripcion")
    recom = models.TextField(verbose_name="Recomendaciones")
    priori_des = models.IntegerField(verbose_name="Prioridad tras intervencion",validators=[MinValueValidator(1),MaxValueValidator(6)])

    
    def __str__(self):
        return str(self.estado_rel) + str(self.priori_des)
    class Meta:
        ordering = ["fecha"]
        verbose_name_plural = "Intervenciones"


class InformeArqueo(models.Model):
    objeto = models.ForeignKey(Objeto,verbose_name="Objeto sobre el que se realiza el informe")
    nombre_res = models.CharField(max_length=30,verbose_name=("Nombre restaurador"))
    ape_res = models.CharField(max_length=50,verbose_name=("Apellidos del restaurador")) 
    diagnostico = models.TextField(verbose_name=("Diagnóstico"))
    proyecto = models.TextField(verbose_name=("Proyecto de intervención"))
    desarrollo = models.TextField(verbose_name=("Desarrollo"))
    fecha =  models.DateField(auto_now=True,verbose_name=("Fecha del informe"))  
    
    def __str__(self):
        return str(self.id) 
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
      return str(self.fecha_prestado) + " "  + str(self.fecha_devuelto) + " " + str(self.expo)
    class Meta:
        ordering = ["fecha_prestado"]
        verbose_name_plural = "Movimientos"
