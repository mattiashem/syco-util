import time
import socket
import re
import os
import StringIO
from EvidenceSettings import *

def write_to_file(filename, from_evidence, infolder, host):


    if host in network:
        folder ="/network/"+infolder

    elif host in application:
        folder ="/application/"+infolder
    else:
        folder = "/plattform/"+infolder
    try:
        if not os.path.exists('togit/' + folder):
            os.makedirs('togit/' + folder)
        f = open('togit/' + folder + '/' + filename + '_' + time.strftime('%d-%m-%Y') + '.txt', 'w')
        try:
            buf = StringIO.StringIO(from_evidence)
            for line in buf:
                line = re.sub('^userPassword.*', 'userPassword:*******', line)
                line = re.sub('^#.*', '', line)
                f.write(line)

        finally:
            f.close()

    except IOError:
        pass