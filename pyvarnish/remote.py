# -*- coding: utf-8 -*-
__author__ = 'John Moylan'

import sys

from paramiko import SSHClient, SSHConfig, AutoAddPolicy

from pyvarnish.settings import SSH_CONFIG


class Varnish_admin():

    def __init__(self, server=''):
        self.server = server
        self.conf = self.config()

    def config(self):
        sshconfig = SSHConfig()
        try:
            sshconfig.parse(open(SSH_CONFIG))
        except IOError:
            print "your app needs to have a valid " \
                  "ssh config file location in settings.py"
            sys.exit(1)
        return sshconfig.lookup(self.server)

    def runcmd(self, cmd):
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(self.conf['hostname'],
                            port = int(self.conf['port']),
                            username = self.conf['user'],
                            key_filename = self.conf['identityfile'],
                            password = None,)
            stdin, stdout, stderr = client.exec_command(cmd)
            return ''.join([i.rstrip('\r\n ').lstrip() for i in stdout.readlines()])
        finally:
            client.close()