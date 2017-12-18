#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from docker_django.apps.Fondos.models import *

from time import time

import csv, re, os, sys, unicodedata

# Clase para poblar la base de datos
class Setup():
	'''Clase para poblar la base de datos'''
	def __init__(self,f):
		os.system('setterm -cursor off')
		self.debug = True
		self.fichero = open(f)
		self.datos = csv.DictReader(self.fichero, delimiter=';' ,quotechar='"')
		self.dict_arq = {}
		self.l_numinv = []
		self.set_dict_arq()
		self.poblacion_completa()
		os.system('setterm -cursor on')

	def set_dict_arq(self):
		for registro in self.datos:
			self.dict_arq[registro['ID']] = {}

	def poblacion_completa(self):
		w = get_terminal_size()[0]
		# Poblar Continente, Pais, comunidad...
		try:
			print "\n"+("\033[33m[ ]\033[0m Población Inicial "+" "*1000)[:w+6]+"\033[35m1/8\033[0m\r",
			sys.stdout.flush()
			self.poblacion_inicial()
			print "\033[32m[+]\033[0m"
		except:
			print "\033[31m[x]\033[0m"
			raise
		# Poblar Materiales
		try:
			print ("\033[33m[ ]\033[0m Población Materiales "+" "*1000)[:w+6]+"\033[35m2/8\033[0m\r",
			sys.stdout.flush()
			self.poblacion_material()
			print "\033[32m[+]\033[0m"
		except:
			print "\033[31m[x]\033[0m"
			raise
		# Poblar Series
		try:
			print ("\033[33m[ ]\033[0m Población Series "+" "*1000)[:w+6]+"\033[35m3/8\033[0m\r",
			sys.stdout.flush()
			self.poblacion_serie()
			print "\033[32m[+]\033[0m"
		except:
			print "\033[31m[x]\033[0m"
			raise
		# Poblar Secciones
		try:
			print ("\033[33m[ ]\033[0m Población Secciones "+" "*1000)[:w+6]+"\033[35m4/8\033[0m\r",
			sys.stdout.flush()
			self.poblacion_seccion()
			print "\033[32m[+]\033[0m"
		except:
			print "\033[31m[x]\033[0m"
			raise
		# Poblar Culturas
		try:
			print ("\033[33m[ ]\033[0m Población Culturas "+" "*1000)[:w+6]+"\033[35m5/8\033[0m\r",
			sys.stdout.flush()
			self.poblacion_cultura()
			print "\033[32m[+]\033[0m"
		except:
			print "\033[31m[x]\033[0m"
			raise
		# Poblar Edades
		try:
			print ("\033[33m[ ]\033[0m Población Edades "+" "*1000)[:w+6]+"\033[35m6/8\033[0m\r",
			sys.stdout.flush()
			self.poblacion_edad()
			print "\033[32m[+]\033[0m"
		except:
			print "\033[31m[x]\033[0m"
			raise
		# Poblar Yacimientos
		try:
			print ("\033[33m[ ]\033[0m Población Yacimientos "+" "*1000)[:w+6]+"\033[35m7/8\033[0m\r",
			sys.stdout.flush()
			self.poblacion_yacimiento()
			print "\033[32m[+]\033[0m"
		except:
			print "\033[31m[x]\033[0m"
			raise
		# Poblar Objetos
		try:
			print ("\033[33m[ ]\033[0m Población Objetos "+" "*1000)[:w+6]+"\033[35m8/8\033[0m\r",
			sys.stdout.flush()
			self.poblacion_objeto()
			print "\033[32m[+]\033[0m"
		except:
			print "\033[31m[x]\033[0m"
			raise

	def poblacion_inicial(self):
		# Limpiar base de datos (sólo depuración)
		if self.debug:
			self.clear_db(Continente.objects.all())
		if not Continente.objects.all():
			# Poblar continentes
			c = Continente(nombre="EUROPA")
			c.save()
			# Poblar paises
			p = Pais(nombre="ESPAÑA",continente=c)
			p.save()
			# Poblar comunidades autónomas
			ca = Ca(nombre="ANDALUCÍA",pais=p)
			ca.save()
			# Poblar provincias
			prc = Provincia(nombre="CÁDIZ",ca=ca)
			prc.save()
			prs = Provincia(nombre="SEVILLA",ca=ca)
			prs.save()
			# Poblar municipios de la provincia de Cádiz
			mc_list = ["ALAMEDA", "ALCALÁ DE GUADAIRA", "ALCALÁ DE LOS GAZULES", "ALGECIRAS", 
			"ARCOS DE LA FRONTERA", "BAILÉN", "BARBATE", "BARBATE - TARIFA", "BORMUJOS", "BORNOS", 
			"CÁDIZ", "CARMONA", "CHICLANA DE LA FRONTERA", "CHIPIONA", "CHIPIONA - ROTA", 
			"CONÍL DE LA FRONTERA", "CORTES", "DOS HERMANAS", "EL BOSQUE", "EL CUERVO", 
			"EL PALMAR DE TROYA", "EL PUERTO DE SANTA MARÍA", "EL PUERTO DE SANTA MARÍA - ROTA", 
			"ESPERA", "ESTEPA", "ESTEPONA", "GELVES", "GRANADA", "GUADAIRA (SAN RQUE)", 
			"GUADALCACIN", "GUADALCACÍN-JEREZ DE LA FRONTERA", "GUADIARO", "ISLA CRISTINA", 
			"JEREZ DE LA FRONTERA", "LA LÍNEA DE LA CONCEPCIÓN", "LAS CABEZAS DE SAN JUAN", 
			"LAS GABIAS", "LEBRIJA", "LEPE", "LINARES", "LOS BARRIOS", "LOS MOLARES", 
			"LOS PALACIOS", "MADRID", "MÁLAGA", "MARIBAÑEZ (LOS PALACIOS)", 
			"MEDINA SIDONIA", "MONREAL DEL CAMPO", "MORÓN DE LA FRONTERA", "OLVERA", 
			"PALMONES(LOS BARRIOS)", "PALOS DE LA FRONTERA", "PATERNA DE LA RIVERA", 
			"POBLADO DE SAN LEANDRO", "PRADO DEL REY", "PUERTO REAL", "ROTA", "SAN FERNANDO", 
			"SAN JOSÉ DEL VALLE", "SAN ROQUE", "SANLÚCAR DE BARRAMEDA", "SEVILLA", 
			"TARAGILLA (SAN ROQUE)", "TARIFA", "TARIFA - VEJER DE LA FRONTERA", "TORRE ALHÁQUIME", 
			"TORRE GUADIARO- SAN ROQUE", "TREBUJENA", "TREBUJENA (PENITA NEGRA)", "UBRIQUE", 
			"UTRERA", "VEJER DE LA FRONTERA", "VILLALUENGA DEL ROSARIO", "VILLAMARTÍN", 
			"ZAHARA DE LA SIERRA", "ZAHORA (BA\033[33m[ ]\033[0mRBATE)"] 
			# Añadir municipio no encontrado
			Municipio(nombre="???",provincia=prc).save()
			for mc in mc_list:
				Municipio(nombre=mc,provincia=prc).save()

	def poblacion_material(self):
		# Limpiar base de datos (sólo depuración)
		if self.debug:
			self.clear_db(Material.objects.all())
		if not Material.objects.all():
			# Obtener y poblar materiales
			self.fichero.seek(0)
			self.fichero.next()
			lista_materiales = []
			for registro in self.datos:
				arq_id = registro['ID']
				self.dict_arq[arq_id]['MATERIALES'] = []
				if registro['MATERIAL']:
					materiales = registro['MATERIAL'].replace('-',',').replace('?','')
					materiales = re.sub('[(]{1}.*[)]{1}','',materiales)
					l_materiales = materiales.split(",") 
					for material in l_materiales:
						if self.fix_str(material) not in lista_materiales:
							lista_materiales.append(self.fix_str(material))
							obj = Material(nombre=self.fix_str(material))
							obj.save()
						else:
							obj = Material.objects.get(nombre=self.fix_str(material))
						self.dict_arq[arq_id]['MATERIALES'].append(obj)

	def poblacion_serie(self):
		# Limpiar base de datos (sólo depuración)
		if self.debug:
			self.clear_db(Serie.objects.all())
		if not Serie.objects.all():
			# Obtener y poblar series
			self.fichero.seek(0)
			self.fichero.next()
			lista_series = []
			null = Serie(nombre="NO ESPECIFICADO")
			null.save()
			for registro in self.datos:
				arq_id = registro['ID']
				if registro['SERIE']:
					serie = registro['SERIE'].replace('?','').replace(' )',')')
					if self.fix_str(serie) not in lista_series:
						lista_series.append(self.fix_str(serie))
						obj = Serie(nombre=self.fix_str(serie))
						obj.save()
					else:
						obj = Serie.objects.get(nombre=self.fix_str(serie))
					self.dict_arq[arq_id]['SERIE'] = obj
				else:
					self.dict_arq[arq_id]['SERIE'] = null

	def poblacion_seccion(self):
		# Limpiar base de datos (sólo depuración)
		if self.debug:
			self.clear_db(Seccion.objects.all())
		if not Seccion.objects.all():
			# Obtener y poblar secciones
			self.fichero.seek(0)
			self.fichero.next()
			lista_secciones = []
			null = Seccion(nombre="NO ESPECIFICADO")
			null.save()
			for registro in self.datos:
				arq_id = registro['ID']
				if registro['SECCION']:
					seccion = registro['SECCION'].replace('?','').replace(' )',')')
					if self.fix_str(seccion) not in lista_secciones:
						lista_secciones.append(self.fix_str(seccion))
						obj = Seccion(nombre=self.fix_str(seccion))
						obj.save()
					else:
						obj = Seccion.objects.get(nombre=self.fix_str(seccion))
					self.dict_arq[arq_id]['SECCION'] = obj
				else:
					self.dict_arq[arq_id]['SECCION'] = null

	def poblacion_cultura(self):
		# Limpiar base de datos (sólo depuración)
		if self.debug:
			self.clear_db(Cultura.objects.all())
		if not Cultura.objects.all():
			# Obtener y poblar culturas
			self.fichero.seek(0)
			self.fichero.next()
			lista_culturas = []
			null = Cultura(nombre="NO ESPECIFICADO")
			null.save()
			for registro in self.datos:
				arq_id = registro['ID']
				if registro['CULTURA']:
					cultura = registro['CULTURA'].replace('?','').replace(' )',')')
					if self.fix_str(cultura) not in lista_culturas:
						lista_culturas.append(self.fix_str(cultura))
						obj = Cultura(nombre=self.fix_str(cultura))
						obj.save()
					else:
						obj = Cultura.objects.get(nombre=self.fix_str(cultura))
					self.dict_arq[arq_id]['CULTURA'] = obj
				else:
					self.dict_arq[arq_id]['CULTURA'] = null

	def poblacion_edad(self):
		# Limpiar base de datos (sólo depuración)
		if self.debug:
			self.clear_db(Edad.objects.all())
		if not Edad.objects.all():
			# Obtener y poblar edades
			self.fichero.seek(0)
			self.fichero.next()
			lista_edades = []
			null = Edad(nombre="NO ESPECIFICADO")
			null.save()
			for registro in self.datos:
				arq_id = registro['ID']
				if registro['EDAD']:
					edad = registro['EDAD'].replace('?','')
					if self.fix_str(edad) not in lista_edades:
						lista_edades.append(self.fix_str(edad))
						obj = Edad(nombre=self.fix_str(edad))
						obj.save()
					else:
						obj = Edad.objects.get(nombre=self.fix_str(edad))
					self.dict_arq[arq_id]['EDAD'] = obj
				else:
					self.dict_arq[arq_id]['EDAD'] = null

	def poblacion_yacimiento(self):
		# Limpiar base de datos (sólo depuración)
		if self.debug:
			self.clear_db(Yacimiento.objects.all())
		if not Yacimiento.objects.all():
			# Obtener y poblar yacimientos
			self.fichero.seek(0)
			self.fichero.next()
			lista_yacimientos = []
			null = Yacimiento(yacimiento="NO ESPECIFICADO",municipio_id=Municipio.objects.get(nombre="???".encode("utf-8")).pk)
			null.save()
			for registro in self.datos:
				arq_id = registro['ID']
				if registro['PROCEDENCIA']:
					yacimiento = self.fix_str(registro['PROCEDENCIA'].replace('?',''))
					yacimiento = self.fix_yacimientos(yacimiento)
					# Comprobar si contiene municipio
					l_municipio = Municipio.objects.all()
					if len(yacimiento) and yacimiento not in lista_yacimientos:
						lista_yacimientos.append(yacimiento)
						mun = None
						for municipio in l_municipio:
							if municipio.nombre.encode("utf-8") in yacimiento:
								# Obtener municipio
								mun = Municipio.objects.get(nombre=municipio.nombre.encode("utf-8"))
								break
						if not mun:
							mun = Municipio.objects.get(nombre="???".encode("utf-8"))
						obj = Yacimiento(yacimiento=self.fix_str(yacimiento),municipio_id=mun.pk)
						obj.save()
						self.dict_arq[arq_id]['YACIMIENTO'] = obj
					else:
						self.dict_arq[arq_id]['YACIMIENTO'] = null
				else:
					self.dict_arq[arq_id]['YACIMIENTO'] = null
			self.fix_yacimientos_2()

	def poblacion_objeto(self):
		# Limpiar base de datos (sólo depuración)
		if self.debug:
			self.clear_db(Objeto.objects.all())
			self.clear_db(Arqueologia.objects.all())
		if not Objeto.objects.all() and not Arqueologia.objects.all():
			# Obtener y poblar objetos/arqueología
			self.fichero.seek(0)
			self.fichero.next()
			lista_objetos = []
			lista_numinv = []
			if not len(Ubicacion.objects.filter(tipo="NO",nombre="ESPECIFICADO")):
				ubicacion_nula = Ubicacion(tipo="NO",nombre="ESPECIFICADO")
				ubicacion_nula.save()
			else:
				ubicacion_nula = Ubicacion.objects.get(tipo="NO",nombre="ESPECIFICADO")
			for registro in self.datos:
				arq_id = registro['ID']
				# Obtener fecha de ingreso y código
				fecha = self.fix_str(registro['FECHA INGRESO'])
				fechadatacion = self.fix_str(registro['FECHA'])
				nombre = self.fix_str(registro['OBJETO'])
				codigo = None
				numero_entrada = None
				# Extraer código, numero de entrada y fecha de ingreso
				if fecha:
					for code in ['DJ/','CE/','DO/','DE/']:
						if code in fecha[:3]:
							numero_entrada = int(fecha[3:5])
							fecha = fecha[6:8]
							codigo = code[:-1]
							break
				fecha_ingreso = fecha
				# Parchear numinv duplicados
				numinv = self.fix_str(registro['NUMINV']).replace("- ","-").replace(" -","-")
				if numinv not in lista_numinv:
					lista_numinv.append(numinv)
				else:
					numinv = str(numinv) + "-B"
					lista_numinv.append(numinv)
				numinv = self.fix_numinv(numinv)
				# Creando Objetos/Arqueología
				arq = Arqueologia(numinv=numinv)
				arq.save_base()
				arq.nombre = nombre
				arq.codigo = codigo
				arq.datacion = fechadatacion
				arq.ubicacion = ubicacion_nula
				arq.fechaingreso = fecha_ingreso
				arq.numero_entrada = numero_entrada
				arq.edad = self.dict_arq[arq_id]['EDAD']
				arq.serie = self.dict_arq[arq_id]['SERIE']
				arq.cultura = self.dict_arq[arq_id]['CULTURA']
				arq.seccion = self.dict_arq[arq_id]['SECCION']
				arq.yacimiento = self.dict_arq[arq_id]['YACIMIENTO']
				arq.material.set(self.dict_arq[arq_id]['MATERIALES'])
				arq.save()

	def fix_str(self, cadena):
		# Prepara un cadena para ser comparada
		cadena = cadena.decode("utf-8").upper()
		cadena = cadena.encode("utf-8").strip()
		cadena = re.sub(' +',' ',cadena)
		return cadena

	def fix_yacimientos(self, yacimiento):
		# Quitar año de yacimiento
		yacimiento = re.sub('\/[0-9\-]{1,}','',yacimiento)
		# Parcheando algunos registros
		if "ARCOS" in yacimiento and "ARCOS DE LA FRONTERA" not in yacimiento:
			yacimiento = yacimiento.replace('ARCOS','ARCOS DE LA FRONTERA')
		if self.fix_str("AVENIDA ANDALUCÍA") in yacimiento and self.fix_str("CÁDIZ") not in yacimiento:
			yacimiento = yacimiento + self.fix_str(". CÁDIZ")
		if self.fix_str("AVENIDA PORTUGAL") in yacimiento and self.fix_str("CÁDIZ") not in yacimiento:
			yacimiento = yacimiento + self.fix_str(". CÁDIZ")
		if self.fix_str("AVENIDA SAN SEVERIANO") in yacimiento and self.fix_str("CÁDIZ") not in yacimiento:
			yacimiento = yacimiento + self.fix_str(". CÁDIZ")
		if self.fix_str("BAELO CLAUDIA") in yacimiento and self.fix_str("TARIFA") not in yacimiento:
			yacimiento = yacimiento + self.fix_str(". TARIFA")
		if self.fix_str("C/ ACACIAS") in yacimiento and self.fix_str("CÁDIZ") not in yacimiento:
			yacimiento = yacimiento + self.fix_str(". CÁDIZ")
		if "VEJER" in yacimiento and "VEJER DE LA FRONTERA" not in yacimiento:
			yacimiento = yacimiento.replace('VEJER','VEJER DE LA FRONTERA')
		return yacimiento

	def fix_yacimientos_2(self):
		# Parcheando un registro
		m = Municipio.objects.get(nombre="PUERTO REAL")
		y = Yacimiento.objects.get(yacimiento="AUTOPISTA CÁDIZ-SEVILLA. PUERTO REAL")
		y.municipio_id = m.pk
		y.save()
		# Parcheando otro registro
		m = Municipio.objects.get(nombre="PATERNA DE LA RIVERA")
		y = Yacimiento.objects.get(yacimiento="C/ PUERTO REAL. PATERNA DE LA RIVERA")
		y.municipio_id = m.pk
		y.save()

	def fix_fecha_ingreso(self,fi):
		fecha = None
		# Extraer y formatear fecha (¡YA NO SE USA!)
		if fi:
			p = re.compile(r'^[0-9]{2}/[0-9]{2}/[0-9]{2}$')
			if p.search(fi):
				p = re.compile(r'\/')
				f = p.split(fi)
				if len(f) == 3:
					if int(f[2]) >= 18:
						fecha = '19'+f[2]+"-"+f[1]+'-'+f[0]
					else:
						fecha = '20'+f[2]+"-"+f[1]+'-'+f[0]
					fi = None
		if fi:
			p = re.compile(r'^[0-9]{2}-[0-9]{2}-[0-9]{4}$')
			if p.search(fi):
				p = re.compile(r'\-')
				f = p.split(fi)
				if len(f) == 3:
					fecha = f[2]+"-"+f[1]+'-'+f[0]
					fi = None
		if fi:
			p = re.compile(r'ANTERIOR|POSTERIOR A [0-9]{4}')
			if p.search(fi):
				fecha = fi[-4:]+"-01-01"
				fi = None
		if fi:
			p = re.compile(r'^[0-9]{4}$')
			if p.search(fi):
				fecha = fi+"-01-01"
				fi = None
		return fecha

	def fix_numinv(self,oldnuminv):
		# Serializar numinv repetidos (¡EXPERIMENTAL!)
		p = re.compile(r'^[0-9]*/|-| [a-zA-Z0-9]*$')  
		if p.search(oldnuminv):
			m = 64
			n = 65
			o = 65
			p = re.compile(r'/|-| ') 
			numinv = p.split(oldnuminv)[0] + "/" + chr(n)    
			while numinv in self.l_numinv:
				if n < 90:
					n += 1
					numinv = p.split(oldnuminv)[0] + "/" + chr(n)
				else:
					if m == 90:
						m = 64
						o += 1
					m += 1
					numinv = p.split(oldnuminv)[0] + "/" + chr(o) + chr(m)
			self.l_numinv.append(numinv)
		else:
			numinv = oldnuminv
		return numinv

	def clear_db(self, datos):
		try:
			for registro in datos:
				registro.delete()
		except:
			pass

# Funciones y procedimentos útiles
def get_terminal_size():
	import fcntl, termios, struct
	h, w, hp, wp = struct.unpack('HHHH',
		fcntl.ioctl(0, termios.TIOCGWINSZ,
		struct.pack('HHHH', 0, 0, 0, 0)))
	return w, h

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

# Clase principal
class Command(BaseCommand):
	help = 'Script para poblar Arqueología'

	def add_arguments(self, parser):
		parser.add_argument('fichero', nargs='+', type=str)

	def handle(self, *args, **options):
		inicio = time() 
		for fichero in options['fichero']:
			Setup(fichero)
		fin = time() 
		tiempo = fin-inicio
		print "\nLa migración se completó en: "  + format_time(tiempo) + "\n"
