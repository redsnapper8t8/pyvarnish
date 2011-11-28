# -*- coding: utf-8 -*-
__author__ = 'John Moylan'
from paramiko import SSHClient, SSHConfig, AutoAddPolicy


class Varnish_admin():

    def __init__(self, server='', cmd='varnishstat -x'):
        self.server = server
        self.cmd = cmd

    def conf(self):
        sshconfig = SSHConfig()
        sshconfig.parse(open('/home/john/.ssh/config'))
        return sshconfig.lookup(self.server)

    def varnishstat(self):
        try:
            client = SSHClient()
            client.load_system_host_keys()
            #client.set_missing_host_key_policy(AutoAddPolicy())
            mconf = self.conf()
            print mconf
            client.connect(mconf['hostname'],
                            port = int(mconf['port']),
                            username = mconf['user'],
                            key_filename = mconf['identityfile'],
                            password = None,)
            stdin, stdout, stderr = client.exec_command(self.cmd)
            data = ''.join([i.rstrip('\r\n ').lstrip() for i in stdout.readlines()])
            return data
        finally:
            client.close()

