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

    def handle(self):
        print "El cliente nos manda:"
        while 1:
            Line = self.rfile.read()
            print Line
            if not Line:
                break
            else:
                List = Line.split(' ')
                Direccion_SIP = List[1].split(':')[1]
                Dic_User[Direccion_SIP] = self.client_address[0]
                self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
                Expires = int(List[3])
                if Expires == 0:
                    del Dic_User[Direccion_SIP]
                print "Los ususarios son:" + '\r\n' + str(Dic_User)

if __name__ == "__main__":
    Dic_User = {}
    PORT = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
