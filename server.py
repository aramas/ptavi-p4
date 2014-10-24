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
            line = self.rfile.read()
            print line
            Lista = line.split(' ')
            TYPE = Lista[0]
            if TYPE == "REGISTER":
                DIREC_SIP = Lista[1].split(':')[1]
                Dic_User[DIREC_SIP] = self.client_address[0]
                self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
                print "Los usuarios son:" + '\r\n' + str(Dic_User)
            if not line:
                break

if __name__ == "__main__":
    Dic_User = {}
    PORT = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
