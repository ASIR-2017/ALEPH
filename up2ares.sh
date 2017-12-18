#!/bin/bash

echo
echo "╔═════════════════════════════════════════════════════════════╗"
echo "║ USO DEL SCRIPT:                                             ║"
echo "║ → Introduce <contraseña> para confirmar la operación actual ║"
echo "║ → Pulsa 'CTRL + C' para saltar/cancelar la operación actual ║"
echo "╚═════════════════════════════════════════════════════════════╝"
echo
echo -e "\033[33m¿Actualizar código?\033[0m"
scp web/docker_django/apps/Fondos/*.py root@ares:/opt/dockyard/ALEPH-2.0/AlephDocker/web/docker_django/apps/Fondos/
echo -e "\033[33m¿Actualizar ficheros?\033[0m"
scp -r web/static/* root@ares:/opt/dockyard/ALEPH-2.0/AlephDocker/web/static/
echo -e "\033[33m¿Actualizar plantillas?\033[0m"
scp -r web/docker_django/apps/Fondos/templates/* root@ares:/opt/dockyard/ALEPH-2.0/AlephDocker/web/docker_django/apps/Fondos/templates/
echo -e "\033[33m¿Reiniciar la aplicación?\033[0m"
ssh root@ares "cd /opt/dockyard/ALEPH-2.0/AlephDocker ; docker-compose restart web nginx"
echo
