from django import forms
from .models import *
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime, timedelta, date
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings

class TicketForm(forms.ModelForm): 
    class Meta:
      model = Ticket
      exclude = ('estado','propietario')
