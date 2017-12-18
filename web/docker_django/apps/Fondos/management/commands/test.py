#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from docker_django.apps.Fondos.models import *

class Command(BaseCommand):
	help = 'Script de ejemplo'

	def handle(self, *args, **options):
		try:
			c = Continente.objects.all()
			for cont in c:
				print cont.nombre
			print "\nTodo va bien.\n"
		except:
			print "\nOcurrió un error inesperado.\n"
			raise
