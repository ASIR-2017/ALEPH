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
#STATIC_ROOT = ''
#STATIC_URL = '/static/'
#STATICFILES_DIRS = (os.path.join('static'), )

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
    'django.contrib.humanize',
#Extra para debug
    'django_extensions',
#Aplicaciones de terceros
    'dal',
    'dal_select2',
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
    #'MENU_EXCLUDE': ('auth.group',),
    #'MENU': (
    #     'sitios',
    #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
    #     {'label': 'Configuracin', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    #     {'label': 'Ayuda', 'icon':'icon-question-sign', 'url': '/support/'},
    #),

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
        'HOST': '10.34.17.11',
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
###### No accesible -> https://pypi.python.org/pypi/django-auth-ldap
#

#le decimos que use unicamente de backend en AD de nuestro servidor
AUTHENTICATION_BACKENDS = (
 'django_auth_ldap.backend.LDAPBackend',
 'django.contrib.auth.backends.ModelBackend',
)

#AUTENTICACION LDAP CON SERVIDOR DE PRUEBA EN WINDOWS 2008 R2 SERVER CON ACTIVE DIRECTORY
import ldap
# For this, you want to be using the -H flag setting you used above.
#AUTH_LDAP_SERVER_URI = os.environ['LDAP_URI']
AUTH_LDAP_SERVER_URI = "ldap://adriano.dca.ccul.junta-andalucia.es:389 ldap://hesperides.dca.ccul.junta-andalucia.es:389"

#bindeo simple de root dn
#AUTH_LDAP_BIND_DN = os.environ['LDAP_BIND_DN']
AUTH_LDAP_BIND_DN = "CN=django,OU=ADMINISTRADORES,DC=dca,DC=ccul,DC=junta-andalucia,DC=es"
#AUTH_LDAP_BIND_PASSWORD = os.environ['LDAP_BIND_PASSWD']
AUTH_LDAP_BIND_PASSWORD = "Cultura2017"

LDAP_IGNORE_CERT_ERRORS = False


from django_auth_ldap.config import LDAPSearch,LDAPSearchUnion,NestedActiveDirectoryGroupType

AUTH_LDAP_USER_SEARCH = LDAPSearchUnion (
    LDAPSearch("ou=ADMINISTRADORES,dc=dca,dc=ccul,dc=junta-andalucia,dc=es", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=MCA_Usuarios,OU=MUSEO,OU=UNIDADES,DC=dca,DC=ccul,DC=junta-andalucia,DC=es", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("OU=Aleph,OU=MCA_Grupos,OU=MUSEO,OU=UNIDADES,DC=dca,DC=ccul,DC=junta-andalucia,DC=es",
                                    ldap.SCOPE_SUBTREE,"(objectClass=group)")

AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType() #GroupOfNamesType()
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600   #cache de una hora
#opcion necesaria
AUTH_LDAP_MIRROR_GROUPS = True
AUTH_LDAP_CONNECTION_OPTIONS = {
ldap.OPT_DEBUG_LEVEL: 1,
ldap.OPT_REFERRALS: 0,}

AUTH_LDAP_USER_ATTR_MAP = {
 "first_name":"givenName", }


#flags por grupo
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
   "is_active": "CN=Aleph_Activos,OU=Aleph,OU=MCA_Grupos,OU=MUSEO,OU=UNIDADES,DC=dca,DC=ccul,DC=junta-andalucia,DC=es",
   "is_staff": "CN=Aleph_Staff,OU=Aleph,OU=MCA_Grupos,OU=MUSEO,OU=UNIDADES,DC=dca,DC=ccul,DC=junta-andalucia,DC=es",
   "is_superuser": "CN=Aleph_Superuser,OU=Aleph,OU=MCA_Grupos,OU=MUSEO,OU=UNIDADES,DC=dca,DC=ccul,DC=junta-andalucia,DC=es",
   #"is_documentador": "CN=Aleph_Documentador,OU=Aleph,OU=MCA_Grupos,OU=MUSEO,OU=UNIDADES,DC=dca,DC=ccul,DC=junta-andalucia,DC=es",
   #"is_restaurBA": "CN=Aleph_RestaurBA,OU=Aleph,OU=MCA_Grupos,OU=MUSEO,OU=UNIDADES,DC=dca,DC=ccul,DC=junta-andalucia,DC=es",
   #"is_restaurARQ": "CN=Aleph_RestaurARQ,OU=Aleph,OU=MCA_Grupos,OU=MUSEO,OU=UNIDADES,DC=dca,DC=ccul,DC=junta-andalucia,DC=es",
}

AUTH_LDAP_REQUIRE_GROUP = "cn=aleph_activos,ou=aleph,ou=mca_grupos,ou=museo,ou=unidades,dc=dca,dc=ccul,dc=junta-andalucia,dc=es"

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
            'level': 'DEBUG',
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
#SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = False



############################## django-auth-ldap ##############################
#if DEBUG:
#    import logging, logging.handlers
#    logfile = "/tmp/django-ldap-debug.log"
#    my_logger = logging.getLogger('django_auth_ldap')
#    my_logger.setLevel(logging.DEBUG)
#
#    handler = logging.handlers.RotatingFileHandler(
#       logfile, maxBytes=1024 * 500, backupCount=5)
#
#    my_logger.addHandler(handler)
############################ end django-auth-ldap ############################
#print >>sys.stderr, "hello world settings"
