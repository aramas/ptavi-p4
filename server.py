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
    SIPRegisterHandler. Registro de dominios SIP
    """
    def register2file(self):
        """
        Archivo de Registros en formato .txt
        """
        Archi = open('registered.txt', 'w')
        for User in Dic_User.keys():
            IP = Dic_User[User][0]
            Time = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.gmtime(Dic_User[User][1]))
            Archi.write(User + '\t' + IP + '\t' + str(Time) + '\r\n')
        Archi.close()

    def handle(self):
        """
        Manejador de registros SIP
        """
        print "El cliente nos manda:"
        while 1:
            Line = self.rfile.read()
            print Line
            if not Line:
                break
            else:
                List = Line.split(' ')
                Direc_SIP = List[1].split(':')[1]
                IP = self.client_address[0]
                Expires = time.time() + int(List[3])
                Dic_User[Direc_SIP] = [IP, Expires]
                self.register2file()
                for User in Dic_User.keys():
                    if time.time() >= Dic_User[User][1]:
                        del Dic_User[User]
                        self.register2file()
                self.wfile.write("SIP/1.0 200 OK\r\n\r\n")

if __name__ == "__main__":
    Dic_User = {}
    PORT = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
