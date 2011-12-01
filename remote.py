# -*- coding: utf-8 -*-
__author__ = 'John Moylan'
from paramiko import SSHClient, SSHConfig, AutoAddPolicy

from settings import SSH_CONFIG


class Varnish_admin():

    def __init__(self, server=''):
        self.server = server
        self.conf = self.config()

    def config(self):
        sshconfig = SSHConfig()
        sshconfig.parse(open("/home/john/.ssh/config"))
        return sshconfig.lookup(self.server)

    def runcmd(self, cmd):
        try:
            client = SSHClient()
            client.load_system_host_keys()
            #client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(self.conf['hostname'],
                            port = int(self.conf['port']),
                            username = self.conf['user'],
                            key_filename = self.conf['identityfile'],
                            password = None,)
            stdin, stdout, stderr = client.exec_command(cmd)
            return ''.join([i.rstrip('\r\n ').lstrip() for i in stdout.readlines()])
        finally:
            client.close()
