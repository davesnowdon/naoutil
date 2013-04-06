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
def create(brokerName):
    '''
    Create a broker with the given name.
    Automatically find out NAO IP and our own IP.
    
    It acts as a context manager. Which means, use it with the 'with' statement. Example:
    
    with broker.create('MyBroker') as myBroker:
        print myBroker.getGlobalModuleList()
        raw_input("Press ENTER to terminate the broker")
    # Outside of the with, the broker has been shutdown.    
    '''
    allNAOs = avahi.findAllNAOs()
    # TODO: improve handling of the avahi return.
    # TODO: all to specify the robot ip/port.
    # TODO: if nothing works, fallback on nao.local/9559
    NAO_IP = allNAOs[0]['ip_address']
    NAO_PORT = allNAOs[0]['naoqi_port']
    # Information concerning our new python broker
    ThisBrokerIP = getLocalIp(NAO_IP)
    ThisBrokerPort = 0
  
    pythonBroker = ALBroker(brokerName, ThisBrokerIP, ThisBrokerPort, NAO_IP, NAO_PORT)
    
    yield pythonBroker
    
    pythonBroker.shutdown()
