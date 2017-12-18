#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys 

SECRET_KEY = os.environ['SECRET_KEY']


ALLOWED_HOSTS=['*']
DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

INSTALLED_APPS = [
#Extra para el admin
    'suitlocale',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#Extra para debug
    'django_extensions',
#Aplicaciones de terceros
    'crispy_forms',
    'bootstrap3',
    'django_filters',
    'widget_tweaks',
    'docker_django.apps.Fondos',
    'docker_django.apps.bug',
]

# Django Suit 
SUIT_CONFIG = {
    # header
     'ADMIN_NAME': 'Administración de Aleph',
     'HEADER_DATE_FORMAT': 'l, j. F Y',
     'HEADER_TIME_FORMAT': 'H:i',

    # formulario
     'SHOW_REQUIRED_ASTERISK': True,  # Default True
     'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
     'SEARCH_URL': '/admin/auth/user/',
     'MENU_ICONS': {
        'sites': 'icon-leaf',
        'auth': 'icon-lock',
     },
     'MENU_OPEN_FIRST_CHILD': True, # Default True
     'MENU_EXCLUDE': ('auth.group',),
     'MENU': (
    #     'sitios',
         {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
         {'label': 'Configuración', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
         {'label': 'Ayuda', 'icon':'icon-question-sign', 'url': '/support/'},
     ),

     'LIST_PER_PAGE': 20
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


ROOT_URLCONF = 'docker_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'docker_django.wsgi.application'
LOGIN_REDIRECT_URL = '/' 


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_SERVICE'],
        'PORT': os.environ['DB_PORT']
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#LOCALES
DEFAULT_CHARSET = 'utf-8'

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SHELL_PLUS = "ipython"

#
##La documentacion sobre este apartado se encuentra en
###http://pythonhosted.org/django-auth-ldap/; he seguido este ejemplo de
##configuracion
#

#le decimos que use unicamente de backend en AD de nuestro servidor
AUTHENTICATION_BACKENDS = (
 'django_auth_ldap.backend.LDAPBackend',
 #~ 'django.contrib.auth.backends.ModelBackend',
)


#AUTENTICACION LDAP CON SERVIDOR DE PRUEBA EN WINDOWS 2008 R2 SERVER CON ACTIVE DIRECTORY
import ldap
# For this, you want to be using the -H flag setting you used above.
AUTH_LDAP_SERVER_URI = "ldap://10.17.11.3:389"

#bindeo simple de root dn
AUTH_LDAP_BIND_DN = os.environ['BIND_DN']
AUTH_LDAP_BIND_PASSWORD = os.environ['BIND_PASSWD']

LDAP_IGNORE_CERT_ERRORS = False


from django_auth_ldap.config import LDAPSearch,NestedActiveDirectoryGroupType

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=MCA_usuarios,ou=Museo,ou=Unidades,DC=junta-andalucia,dc=es",
        ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")

#AUTH_LDAP_USER_DN_TEMPLATE = "cn=%(user)s,ou=Museo,ou=Unidades,dc=junta-andalucia,dc=es"

AUTH_LDAP_USER_ATTR_MAP = {
 "first_name":"givenName", }

AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=MCA_Grupos,ou=Museo,ou=Unidades,dc=junta-andalucia,dc=es",
ldap.SCOPE_SUBTREE,"(objectClass=group)")
AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()#GroupOfNamesType()

#flags por grupo
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
  "is_active":"cn=Activos,ou=MCA_Grupos,ou=Museo,ou=Unidades,dc=junta-andalucia,dc=es",
  "is_staff": "cn=Administradordca,ou=MCA_Grupos,ou=Museo,ou=Unidades,dc=junta-andalucia,dc=es",
  "is_superuser": "cn=Administradordca,ou=MCA_Grupos,ou=Museo,ou=Unidades,dc=junta-andalucia,dc=es",
  "is_documentador": "cn=Documentador,ou=MCA_Grupos,ou=Museo,ou=Unidades,dc=junta-andalucia,dc=es",
  "is_restaurBA": "cn=Restauración,ou=MCA_Grupos,ou=Museo,ou=Unidades,dc=junta-andalucia,dc=es",
  "is_restaurARQ": "cn=Arqueologia,ou=MCA_Grupos,ou=Museo,ou=Unidades,dc=junta-andalucia,dc=es",}
  
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600
#cache de una hora


#busqueda de usuarios
LDAP_DOMAIN_BASE = "dc=junta-andalucia,dc=es"
LDAP_USERS_BASE = "ou=MCA_usuarios," + LDAP_DOMAIN_BASE
LDAP_INVENTARIO_BASE = "ou=InventarioRegistro," + LDAP_USERS_BASE
LDAP_RESTAURADORBA_BASE = "ou=Restauracion," + LDAP_USERS_BASE
LDAP_RESTAURADORARQ_BASE = "ou=Arqueologia," + LDAP_USERS_BASE

#opcion necesaria
AUTH_LDAP_CONNECTION_OPTIONS = {
ldap.OPT_DEBUG_LEVEL: 1,
ldap.OPT_REFERRALS: 0,}

#debug para testeo
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'stream_to_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_auth_ldap': {
            'handlers': ['stream_to_console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
