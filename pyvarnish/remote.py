# -*- coding: utf-8 -*-
__author__ = 'John Moylan'

import sys

from paramiko import SSHClient, SSHConfig, AutoAddPolicy

from pyvarnish.settings import SSH_CONFIG


class Varnish_admin():

    def __init__(self, server=''):
        self.server = server
        self.conf = {
            'hostname': server,
            'port': 22,
            # If these are None, Paramiko will figure out the correct values.
            'user': None,
            'identityfile': None,
        }
        self.conf.update(self.config())

    def config(self):
        sshconfig = SSHConfig()
        try:
            sshconfig.parse(open(SSH_CONFIG))
        except IOError:
            sys.stderr.write("Warning: SSH config file location invalid.\n")
        conf = sshconfig.lookup(self.server)
        if 'port' in conf:
            conf['port'] = int(conf['port'])
        
        return conf

    def runcmd(self, cmd):
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(self.conf['hostname'],
                            port = self.conf['port'],
                            username = self.conf['user'],
                            key_filename = self.conf['identityfile'],)
            stdin, stdout, stderr = client.exec_command(cmd)
            return ''.join([i.rstrip('\r\n ').lstrip() for i in stdout.readlines()])
        finally:
            client.close()

