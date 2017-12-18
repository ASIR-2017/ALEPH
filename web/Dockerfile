FROM python:2.7-onbuild

ENV LANG=C.UTF-8
ENV TERM=xterm

RUN apt-get update

# Instalar de dependencias de python
RUN apt-get install -qy python \
                        python-dev \
                        python-pip \
                        python-setuptools \
                        build-essential 

# Instalar dependencias y utlidades del sistema
RUN apt-get install -qy nano\
                        wget \
                        net-tools \
                        git \
                        gcc \
                        libsasl2-dev \
                        python-dev \
                        libldap2-dev \
                        libssl-dev

RUN pip install python-ldap
RUN pip install django-auth-ldap

RUN chown -R www-data:www-data ./static  
RUN chown -R www-data:www-data ./media  
