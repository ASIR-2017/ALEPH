FROM nginx:1.12

RUN apt-get update 


RUN apt-get install openssl

RUN rm /etc/nginx/nginx.conf

ADD conf/ /etc/nginx/
COPY /ssl/* /etc/nginx/
