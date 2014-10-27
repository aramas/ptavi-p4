#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    dic_client = {}
    def handle(self):
        print self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            mensaje = self.rfile.read()
            if not mensaje:
                break
            lista_mensaje = mensaje.split(" ")
            Sip = lista_mensaje[1]
            self.dic_client[Sip] = self.client_address[0]
            if lista_mensaje[0] == "REGISTER":
                self.wfile.write(lista_mensaje[2] + " 200 " + 'OK\r\n\r\n')
            # Borramos en caso de expires 0
            if int(lista_mensaje[4]) == 0:
                del self.dic_client[Sip]
            print mensaje + " " + lista_mensaje[2] + '\r\n\r\n'
            print self.dic_client

PUERTO = int(sys.argv[1])

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PUERTO), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
