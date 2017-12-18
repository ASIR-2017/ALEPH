#!/usr/bin/env python
# -*- coding: utf-8 -*

from django.contrib.auth.decorators import user_passes_test

'''

FUNCIÓN QUE ACTÚA COMO UN DECORADOR EN EL FICHERO
VIEWS QUE MIRA SI EL NOMBRE DEL USUARIO AUTENTICADO ESTÁ
EN UN GRUPO. SI PERTENECE O EL USUARIO ES SUPERUSUARIO SE LE PERMITE
EL ACCESO A LA ZONA DE LA APLICACIÓN. EN CASO CONTRARIO SE MOSTRARÁ LA PLANTILLA DE ERROR
ERROR.HTML.

'''


def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='/error/')
