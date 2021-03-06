#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

lista = sys.argv
# Comprobamos si hemos pasado los datos adecuados por linea de comandos.
if len(lista) != 6:
    print "Usage: client.py ip puerto register sip_address expires_value"
    raise SystemExit
SERVER = lista[1]
PORT = int(lista[2])
VERSION = "SIP/2.0"

# Contenido que vamos a enviar
PETICION = lista[3]
CLIENTE = lista[4]
TIEMPO = lista[5]
ENVIO = PETICION.upper() + " " + CLIENTE + " " + VERSION + ' \r\n'
ENVIO += "Expires: " + TIEMPO

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + ENVIO
my_socket.send(ENVIO)
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
