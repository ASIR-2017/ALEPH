#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from django.utils.encoding import uri_to_iri, iri_to_uri

from django.core.files import File

from django.core.files.temp import NamedTemporaryFile

from docker_django.apps.Fondos.models import *

from bs4 import BeautifulSoup

import urllib2, random, time, sys, re

# Constantes
HTTP_PROXY = '10.34.0.17:3128'

# Variables
debug = False
set_proxy = True
registros = []

# Funciones
def format_time(tt):
	t = {'H':0,'M':0,'S':0}
	while tt >= 3600:
		tt = tt - 3600
		t['H'] = t['H'] + 1
	while tt >= 60:
		tt = tt - 60
		t['M'] = t['M'] + 1
	t['S'] = int(tt)
	result = ""
	if t['H']:
		result = result + str(t['H']) + " horas "
	if t['M']:
		result = result + str(t['M']) + " minutos "
	if t['S']:
		result = result + str(t['S']) + " segundos "
	return result[:-1]

def fix_string(cadena):
	return re.sub(' +',' ',cadena.decode('utf-8').upper().encode('utf-8'))

# Clases
class ScrapBA:
	'''Clase Scrap para Bellas Artes'''
	def __init__(self,url):
		if set_proxy:
			proxy = urllib2.ProxyHandler({'http':HTTP_PROXY})
			opener = urllib2.build_opener(proxy)
			urllib2.install_opener(opener)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		html = response.read()
		soup = BeautifulSoup(html,'html.parser')
		self.__buscar_obras(soup,url)

	def __buscar_obras(self,soup,url):
		obras = soup.find_all('div', attrs={'class': 'contenedorTextoLPR1'})
		for obra in obras:
			parrafo = obra.find_all('p', attrs={'class': 'gris'})[1]
			try:
				enlace = parrafo.find_all('a')[2]
				pages = 2
			except:
				try:
					enlace = parrafo.find_all('a')[1]
					pages = 7
				except:
					enlace = "dummy"
					pages = 0
			ficha = iri_to_uri("http://ceres.mcu.es/pages/"+enlace['href'].encode('cp1252'))
			for page in range(pages):
				self.__leer_obra(ficha+"page="+str(page+1))

	def __leer_obra(self,url):
		if set_proxy:
			proxy = urllib2.ProxyHandler({'http':HTTP_PROXY})
			opener = urllib2.build_opener(proxy)
			urllib2.install_opener(opener)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		html = response.read()
		soup = BeautifulSoup(html,'html.parser')
		self.__buscar_datos(soup,url)

	def __buscar_datos(self,soup,url):
		fotos = soup.find_all('img', attrs={'class': 'foto'})
		for foto in fotos:
			numinv = foto['title'].split()[-1]
			if numinv not in registros:
				registros.append(numinv)
				codigo = self.__obtener_codigo(numinv)
				titulo = "(?)"
				dimensiones = (0, 0)
				fechaingreso = None
				datacion = ""
				descripcion = ""
				observaciones = ""
				soporte = ""
				iconografias = []
				tecnicas = []
				all_row = soup.find_all('th', attrs={'class': 'tabla1TituloMB'})
				for row in all_row:
					if 'Título' in row.text.encode('utf-8').strip():
						if numinv in row.parent.td['headers'][0]:
							titulo = row.parent.td.text.encode('utf-8').strip()
					if 'Dimensiones' in row.text.encode('utf-8').strip():
						if numinv in row.parent.td['headers'][0]:
							aux = row.parent.td.text.encode('utf-8').strip()
							dimensiones = self.__obtener_dimensiones(aux)
					if 'Datación' in row.text.encode('utf-8').strip():
						if numinv in row.parent.td['headers'][0]:
							datacion = row.parent.td.text.encode('utf-8').strip()
							datacion = re.sub('[(]{1}.*[)]{1}','',datacion).strip()
					if 'Descripción' in row.text.encode('utf-8').strip():
						if numinv in row.parent.td['headers'][0]:
							descripcion = row.parent.td.text.encode('utf-8').strip()
					if 'Observaciones' in row.text.encode('utf-8').strip():
						if numinv in row.parent.td['headers'][0]:
							observaciones = row.parent.td.text.encode('utf-8').strip()
					if 'Materia/Soporte' in row.text.encode('utf-8').strip():
						if numinv in row.parent.td['headers'][0]:
							soporte = row.parent.td.text.encode('utf-8').strip()
							soporte = re.sub('[\[]{1}.*[\]]{1}','',soporte).strip()
					if 'Iconografia' in row.text.encode('utf-8').strip():
						if numinv in row.parent.td['headers'][0]:
							iconografia = row.parent.td.text.encode('utf-8').strip()
							iconografias = iconografia.replace('  ',';').split(';')
					if 'Técnica' in row.text.encode('utf-8').strip():
						if numinv in row.parent.td['headers'][0]:
							tecnica = row.parent.td.text.encode('utf-8').strip()
							tecnicas = tecnica.replace('  ',';').split(';')
					img_url = "http://ceres.mcu.es/pages/Viewer?accion=42&Museo=&AMuseo=MCA&Ninv="+numinv
				if debug:
					print '\n\033[1m\033[33m' + codigo[0] + codigo[1] + "\033[0m"
					print 'Título: ' + fix_string(titulo)
					print 'Altura: ' + str(dimensiones[0]) + ' cm'
					print 'Anchura: ' + str(dimensiones[1]) + ' cm'
					print 'Datación: ' + fix_string(datacion)
					print 'Descripción: ' + fix_string(descripcion[:75]) + "..."
					print 'Observaciones: ' + fix_string(observaciones[:75]) + "..."
					print 'Soporte: ' + fix_string(soporte)
					if iconografias:
						print 'Iconografías: '
					for iconografia in iconografias:
						print fix_string('\t'+iconografia[:30].strip())
					if tecnicas:
						print 'Técnicas: '
					for tecnica in tecnicas:
						print fix_string('\t'+re.sub('[\[]{1}.*[\]]{1}','',tecnica)[:30].strip())
					print 'Imagen: ' + img_url
				else:
					try:
						print "\033[33m[ ]\033[0m " + codigo[0] + codigo[1] + "\r",
						sys.stdout.flush()
						s = Soporte.objects.filter(nombre=fix_string(soporte))
						if len(s):
							objSoporte = s[0]
						else:
							if len(soporte) and len(soporte) <= 30:
								objSoporte = Soporte(nombre=fix_string(soporte))
								objSoporte.save()
							else:
								objSoporte = None
						setIconografias = []
						for iconografia in iconografias:
							if len(iconografia) and len(iconografia) <= 30:
								i = Iconografia.objects.filter(nombre=fix_string(iconografia.strip()))
								if len(i):
									objIconografia = i[0]
								else:
									objIconografia = Iconografia(nombre=fix_string(iconografia.strip()))
									objIconografia.save()
								setIconografias.append(objIconografia)
						setTecnicas = []
						for tecnica in tecnicas:
							tecnica = re.sub('[\[]{1}.*[\]]{1}','',tecnica)
							if len(tecnica) and len(tecnica) <= 30:
								t = Tecnica.objects.filter(nombre=fix_string(tecnica.strip()))
								if len(t):
									objTecnica = t[0]
								else:
									objTecnica = Tecnica(nombre=fix_string(tecnica.strip()))
									objTecnica.save()
								setTecnicas.append(objTecnica)
						arq = Arqueologia.objects.filter(numinv=codigo[1])
						if len(arq):
							arq[0].delete()
						ba = Bellasartes(numinv=codigo[1])
						ba.save_base()
						ba.titulo = fix_string(titulo).split(";")[0][:100]
						ba.codigo = fix_string(codigo[0])
						ba.altura = dimensiones[0]
						ba.ancho = dimensiones[1]
						ba.datacion = fix_string(datacion).replace('=','-')
						ba.descripcion = fix_string(descripcion)
						ba.observaciones = fix_string(observaciones)
						ba.fechaingreso = fechaingreso
						ba.iconografia.set(setIconografias)
						ba.tecnica.set(setTecnicas)
						try:
							ba.soporte = objSoporte
						except:
							pass
						try:
							img_temp = NamedTemporaryFile(delete=True)
							img_temp.write(urllib2.urlopen(img_url).read())
							img_temp.flush()
							ba.anverso.save(codigo[0]+'.jpg', File(img_temp))
						except:
							pass
						ba.save()
						print "\033[32m[+]\033[0m"
					except:
						print "\033[31m[x]\033[0m"

	def __obtener_codigo(self,numinv):
		try:
			int(numinv[:2])
			return (None, numinv)
		except:
			return (numinv[:2],numinv[2:])

	def __obtener_dimensiones(self,bloque):
		try:
			sp = bloque.replace(';','').split(' ')
			s1 = sp[2].replace(',','.')
			m1 = sp[3]
			s2 = sp[6].replace(',','.')
			m2 = sp[7]
			if m1.strip() == 'm':
				altura = float(s1) * float(100)
			else:
				altura = float(s1)
			if m2.strip() == 'm':
				anchura = float(s2) * float(100)
			else:
				anchura = float(s2)
			return (altura, anchura)
		except:
			return (0, 0)

# Comando
class Command(BaseCommand):
	help = 'Busca y puebla Bellas Artes desde Ceres'

	def add_arguments(self, parser):
		parser.add_argument('url', nargs='+', type=str)

	def handle(self, *args, **options):
		inicio = time.time() 
		for url in options['url']:
			for page in range(12):
				try:
					os.system('setterm -cursor off')
					ScrapBA(url+"&page="+str(page+1))
				except:
					os.system('setterm -cursor on')
		fin = time.time()
		tiempo = fin-inicio
		print "\nSe añadieron " + str(len(registros)) + " registros en: "  + format_time(tiempo) + "\n"
