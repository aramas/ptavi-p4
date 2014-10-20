#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        #Mandamos el cliente una notificación que le informa
        #de que hemos recibido su petición
        self.wfile.write("Hemos recibido tu peticion")
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            else:
                print "El cliente nos manda " + line

if __name__ == "__main__":
    #Extraer el dato dle puerto
    PORT = int(sys.argv[1])
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), EchoHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
