###
#
# COPY this file to EvidenceSettings.py before you use the script
#
from __future__ import with_statement
from fabric.api import local, settings, abort
from fabric.contrib.console import confirm
from fabric.api import *

env.roledefs = {
    'test':['192.168.3.2'],


    'hosts': ['10.1.1.1',
            '10.1.1.5',
            '10.1.1.7',
            '10.1.1.12',
            '10.1.1.125',
            '10.1.1.3',
            '10.1.2.105',
            '10.1.2.4',
            '10.1.2.10',
            '10.1.2.115',
            '10.1.2.2',
            '10.1.2.1',
            '10.101.2.108'],

#Setuser name if not used ssh login username
env.user = 'username'