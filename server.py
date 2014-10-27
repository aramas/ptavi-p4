#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

from threading import Timer
import os
import time
import sys
import SocketServer

d = {}
diccionariologout = {}


def register2file(self):
    archi = open('registered.txt', 'w')
    archi.write('User\tIP\tExpires\r\n')
    claves = d.keys()
    for key in claves:
        archi.write(key + '\t' + d[key] + '\t' + str(diccionariologout[key]) + '\r\n')
    archi.close()


def expulsar(self):
    claves = d.keys()
    for key in claves:
        if diccionariologout[key] < (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))):
            del d[key]
            del diccionariologout[key]
    register2file(self)


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        line = self.rfile.read()
        primerparametro = str(line.split(" ")[0])

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            cliente = self.client_address
            ip = str(cliente[0])
            puerto = int(cliente[1])
            if primerparametro == "REGISTER":
                emailsinsip = str(line.split(":")[1])
                email = str(emailsinsip.split(" ")[0])
                d[email] = str(ip)
                # print d
                line2 = line.split(":")
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                if len(line2) == 3:
                    corta1 = str(line.split(":")[1])
                    corta2 = str(corta1.split("\n")[1])
                    if corta2 == "Expires":
                        tiempoexpiracion = float(line.split(":")[2])
                        # print tiempoexpiracion
                        # print email
			if tiempoexpiracion == 0:
				tiempoexpiracion = -1
                        diccionariologout[email] = (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()+int(tiempoexpiracion))))
                        # print diccionariologout
                        expulsar(self)

                break
            else:
                if line:
                    print "El cliente nos manda " + line
                    self.wfile.write("Hemos recibido tu peticion")
                    break
                if not line:
                    break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
