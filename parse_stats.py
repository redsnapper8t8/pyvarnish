# -*- coding: utf-8 -*-
__author__ = 'John Moylan'
__version__ = 0.5
import select
import time
import sys
import time
from StringIO import StringIO
from socket import socket

from lxml import etree

import settings
from remote import Varnish_admin

sock = socket()

CARBON_SERVER = settings.CARBON_SERVER
CARBON_PORT = settings.CARBON_PORT
VARNISH_SERVERS = settings.VARNISH_SERVERS

try:

  sock.connect((CARBON_SERVER, CARBON_PORT))
except:
  print "Couldn't connect to %(server)s on port %(port)d," + \
        "is carbon-agent.py running?" % {
        'server':CARBON_SERVER, 'port':CARBON_PORT}
  sys.exit(1)

class VarnishXMLParser():

    def __init__(self, server, xml):
        self.xml = xml
        self.server_name = server.replace('.','_')

    def parse(self):
        tree = etree.parse(self.xml)
        root = tree.getroot()

        stat_time = root.get('timestamp')
        epochstamp = time.mktime(time.strptime(stat_time, '%Y-%m-%dT%H:%M:%S'))

        lines = []
        for node in root:
            for stat in  node:
                if stat.tag == "name" and stat.getnext().tag == "value":
                    lines.append('varnish.%s.%s %s %d' % (self.server_name, stat.text,
                            stat.getnext().text, int(epochstamp)))
        message = '\n'.join(lines) + '\n' #all lines must end in a newline

        if settings.DEBUG:
            print "sending message\n"
            print '-' * 80
            print message
            print
        sock.sendall(message)

def main():
    for server in VARNISH_SERVERS:
        xml = StringIO(Varnish_admin(server).varnishstat())
        print xml
        VarnishXMLParser(server, xml).parse()

if __name__ == "__main__":
    main()

