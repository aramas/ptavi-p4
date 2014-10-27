#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import sys
import socket

# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = str(sys.argv[1])
PORT = int(sys.argv[2])
LINE = ''
print str(len(sys.argv))
# Contenido que vamos a enviar
for i in sys.argv[3:]:
	LINE = LINE + " " + str(i)

# LINE = '¡Hola mundo!'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + LINE
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
