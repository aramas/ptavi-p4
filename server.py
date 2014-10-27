#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    dic_client = {}
    datos_cliente = []

    def register2file(self):
        """
        Metodo para copiar los datos de los usuarios a un archivo
        """
        fich = open("registered.txt", "w")
        CAMPOS = "User" + '\t' + "IP" + '\t' + "Expires" + '\r\n'
        fich.write(CAMPOS)
        for Usuario in self.dic_client.keys():
            fich.write(Usuario + '\t' + self.dic_client[Usuario][0] + '\t'
                 + time.strftime('%Y-%m-%d %H:%M:%S', \
                 time.gmtime(self.dic_client[Usuario][1]))
                 + '\r\n')

    def handle(self):
        """
        Metodo para manejar los datos de los usuarios
        """
        print self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            mensaje = self.rfile.read()
            if not mensaje:
                break
            lista_mensaje = mensaje.split(" ")
            Sip = lista_mensaje[1]
            Expire = lista_mensaje[4]
            if lista_mensaje[0] == "REGISTER":
                ip = self.client_address[0]
                hora_exp = int(time.time()) + int(Expire)
                self.datos_cliente = [ip, hora_exp]
                self.dic_client[Sip] = self.datos_cliente
                self.wfile.write(lista_mensaje[2] + " 200 " + 'OK\r\n\r\n')
            # Borramos en caso de expires 0
            for Usuario in self.dic_client.keys():
                if int(time.time()) >= self.dic_client[Usuario][1]:
                    del self.dic_client[Usuario]
            print mensaje + '\r\n\r\n'
            print self.dic_client
            self.register2file()

PUERTO = int(sys.argv[1])

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PUERTO), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
