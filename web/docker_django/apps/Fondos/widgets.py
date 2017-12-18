#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
import django.forms as forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from dal.autocomplete import ModelSelect2, ModelSelect2Multiple
from django.utils.translation import ugettext, ugettext_lazy as _

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

class FilteredSelectMultipleWithPop(FilteredSelectMultiple):
   def render(self, name, *args, **kwargs):
      html = super(FilteredSelectMultiple, self).render(name, *args, **kwargs)
      popupplus = render_to_string("widget/popupplus.html", {'field': name})
      return _(html+popupplus)

class ModelSelect2WithPop(ModelSelect2):
   def render(self, name, *args, **kwargs):
      html = super(ModelSelect2, self).render(name, *args, **kwargs)
      popupplus = render_to_string("widget/popupplus.html", {'field': name})
      return _(html+popupplus)

class ModelSelect2MultipleWithPop(ModelSelect2Multiple):
   def render(self, name, *args, **kwargs):
      html = super(ModelSelect2Multiple, self).render(name, *args, **kwargs)
      popupplus = render_to_string("widget/popupplus.html", {'field': name})
      return _(html+popupplus)
