PyVarnish
=========

PyVarnish is a collection of python management tools for Varnish

Currently it only sends Varnish stat output to Graphite.

Screenshots
-----------

.. image:: http://www.8t8.eu/img/graphite.png


Status
------
This software is used in production and works. Documentation and tests are a work
in progress. If you have any questions please feel free to contact me. Any
contributions are also welcomed.

Resources
---------

* `Bug Tracker <http://github.com/redsnapper8t8/pyvarnish/issues>`_
* `Code <http://github.com/redsnapper8t8/pyvarnish>`_
* `My Blog <http://www.8t8.eu>`_


PyVarnish is a Console App
--------------------------

The PyVarnish package is designed to be run at intervals from crontab. It runs varnishstat on
remote varnish servers using SSH commands and sends the data it receives to a
Graphite server over UDP.

Installation
------------

This guide assumes that you already have a Graphite server set up.
Graphite: http://graphite.wikidot.com/

It also assumes familiarity with SSH. In order to run properly PyVarnish needs
to be able to run command remotely. The recommended way to do this is to set up
a restricted account on each of your varnish servers with permission to run a
single command

Below is an example of ssh authorized_keys file for the graphite user on your
varnish server.

``command="/usr/local/bin/graphitewrapper.sh",no-port-forwarding,no-X11-forwarding,no-pty ssh-rsa  publickey```


/usr/local/bin/graphitewrapper.sh might look like this ::


    #!/bin/sh
    # http://binblog.info/2008/10/20/openssh-going-flexible-with-forced-commands/
    case "$SSH_ORIGINAL_COMMAND" in
        "varnishstat -x")
                varnishstat -x
                ;;
        "sysctl fs.file-nr")
                /sbin/sysctl fs.file-nr
                ;;
        *)
                exit 1
                ;;
    esac



To install the PyVarnish package
--------------------------------

from github ::

    pip install https://github.com/redsnapper8t8/pyvarnish/zipball/master

or simply download to a local directory and run from there.

Once installed you need to edit settings.py ::


    VARNISH_SERVERS = ('server1', "server2",)
    SSH_CONFIG = "/home/username/.ssh/config"
    DEBUG = True
    CARBON_SERVER = 'localhost'
    CARBON_PORT = 2003


* Replace server1, server2 etc with the hostnames of your own varnish servers
* SSH_CONFIG needs to refer to your .ssh/config file
* CARBON_SERVER and CARBON_PORT should refer to your graphite server.

Then create a script that runs from crontab to run parse_stats.py

