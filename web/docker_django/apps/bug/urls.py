#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from .views import *

urlpatterns = [
    url(r'^crear_ticket',ticket_crear, name='index'),
    url(r'^ver_mis_tickets',ver_incidencias, name='ver_tickets')
    ]
