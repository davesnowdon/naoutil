# Copyright 2013 Axel Voitier
# All rights reserved (until a FOSS licence is found)

import socket
from contextlib import contextmanager
from naoqi import ALBroker
from naoutil import avahi

def getLocalIp(destAddr):
    '''
    Return the IP of the *net interface capable of reaching destAddr.
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((destAddr, 0))
    ip = s.getsockname()[0]
    s.close()
    return ip

@contextmanager
def create(brokerName, naoIp=None, naoPort=None, brokerIp=None, brokerPort=0):
    '''
    Create a broker with the given name.
    Automatically find out NAO IP and our own IP.
    
    It acts as a context manager. Which means, use it with the 'with' statement. Example:
    
    with broker.create('MyBroker') as myBroker:
        print myBroker.getGlobalModuleList()
        raw_input("Press ENTER to terminate the broker")
    # Outside of the with, the broker has been shutdown.    
    '''
    # Resolve NAO ip/port
    if naoIp is None:
        naoPort = None # Ensure consistency. Do not support specifying only port.
    else:
        naoIp = str(naoIp)
    if naoPort is None:
        allNaos = avahi.findAllNAOs()
        if naoIp is not None: # A NAO address is given, but not the port. Find it.
            for aNao in allNaos:
                if naoIp in aNao.values():
                    naoPort = aNao['naoqi_port']
                    break
            if naoPort is None: # Can't find it in Avahi results
                naoPort = 9559 # Try default port
        else: # Find the most likely NAO
            for aNao in allNaos:
                if aNao['local']: # Prefer to connect to the local naoqi if there
                    naoIp = aNao['ip_address']
                    naoPort = aNao['naoqi_port']
                    break
            if naoIp is None: # No local NAO detected
                if allNaos: # Try to get the first NAO detected by Avahi
                    naoIp = allNaos[0]['ip_address']
                    naoPort = allNaos[0]['naoqi_port']
                else: # Fallback on nao.local/9559
                    naoIp = 'nao.local'
                    naoPort = 9559
    else:
        naoPort = int(naoPort)
                
    # Information concerning our new python broker
    if brokerIp is None:
        brokerIp = getLocalIp(naoIp)
  
    pythonBroker = ALBroker(brokerName, brokerIp, brokerPort, naoIp, naoPort)
    
    yield pythonBroker
    
    pythonBroker.shutdown()
