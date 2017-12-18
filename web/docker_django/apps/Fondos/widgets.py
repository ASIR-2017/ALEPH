#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
import django.forms as forms

#Widget para añadir campos mediante la apertura de un pop-up

class SelectWithPop(forms.Select):
  def render(self, name, *args, **kwargs):
    html = super(SelectWithPop, self).render(name, *args, **kwargs)
    popupplus = render_to_string("widget/popupplus.html", {'field': name})
    return html+popupplus

class MultipleSelectWithPop(forms.SelectMultiple):
   def render(self, name, *args, **kwargs):
      html = super(MultipleSelectWithPop, self).render(name, *args, **kwargs)
      popupplus = render_to_string("widget/popupplus.html", {'field': name})
      return html+popupplus
