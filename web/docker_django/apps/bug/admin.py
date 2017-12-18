from django.contrib import admin
from .models import *

class AdminTicket(admin.ModelAdmin):
 list_display = ["asunto","descripcion","estado","propietario"]
 list_filter = ["estado","propietario"]
 class Meta:
     model = Ticket
#admin.site.register(Ticket,AdminTicket)
