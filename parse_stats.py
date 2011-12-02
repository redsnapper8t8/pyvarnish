# -*- coding: utf-8 -*-
__author__ = 'John Moylan'
__version__ = 0.5
import select
import time
import time
from StringIO import StringIO
import socket

from lxml import etree

from settings import CARBON_SERVER, CARBON_PORT, VARNISH_SERVERS
from remote import Varnish_admin


class VarnishGather():

    def __init__(self, server):
        self.server_name = server.replace('.','_')
        self.lines = []

    def parse_xml(self, xml):
        tree = etree.parse(xml)
        root = tree.getroot()

        stat_time = root.get('timestamp')
        epochstamp = time.mktime(time.strptime(stat_time, '%Y-%m-%dT%H:%M:%S'))

        lines = []
        for node in root:
            for stat in  node:
                if stat.tag == "name" and stat.getnext().tag == "value":
                    self.lines.append('varnish.%s.%s %s %d' % (self.server_name, stat.text,
                            stat.getnext().text, int(epochstamp)))

    def parse_sysctl(self, input):
        epochstamp = int(time.time())
        key = "varnish.%s.%s_current" % (self.server_name, input.split()[0].replace('.','_'))
        value = input.split()[2]
        #append current useage
        self.lines.append("%s %s %d" % (key, value, epochstamp))

        key = "varnish.%s.%s_total" % (self.server_name, input.split()[0].replace('.','_'))
        value = input.split()[4]
        #append total useage
        self.lines.append("%s %s %d" % (key, value, epochstamp))





def msg(message):
    return '\n'.join(message) + '\n'


def main():

    for server in VARNISH_SERVERS:
        #connect to server
        vserver = Varnish_admin(server)

        #run command
        data = vserver.runcmd("varnishstat -x")

        #print data
        xml = StringIO(data)

        vg = VarnishGather(server)

        #parseXML
        vg.parse_xml(xml)

        #get fildescriptors counter
        vg.parse_sysctl(vserver.runcmd("sysctl fs.file-nr"))

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            for i in range(0, len(vg.lines), 50):
                sock.sendto( msg(vg.lines[i:i+50]), (CARBON_SERVER, CARBON_PORT) )
        except:
            import sys, traceback
            print "failed"
            traceback.print_exc(file=sys.stdout)
        finally:
            sock.close()


if __name__ == "__main__":
    main()

