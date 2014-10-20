#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys


VERSION = "SIP/1.0"
class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        dic_client = {}
        self.wfile.write(VERSION + " 200 " + 'OK\r\n\r\n')
        print self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            mensaje = self.rfile.read()
            if not mensaje:
                break
            lista_mensaje = mensaje.split(" ")
            dic_client[lista_mensaje[1]] = self.client_address[0]
            print mensaje + " " + VERSION + '\r\n\r\n'

PUERTO = int(sys.argv[1])

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PUERTO), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
