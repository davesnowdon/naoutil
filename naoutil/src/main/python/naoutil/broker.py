'''
Created on April 05, 2013

@author: AxelVoitier
@license: GNU LGPL v3

Python module allowing to create a ALBroker as if it was a
contextmanager (use with the 'with' statement).
It will also try to resolve automatically all IPs and ports of NaoQis
we could connect to.
'''

import socket
import warnings
from contextlib import contextmanager

from naoqi import ALBroker

from naoutil import avahi


# Since Python 2.7 DeprecationWarning are hidden.
# Force to show them as we throw some. Sorry for the intrusion.
# It could be handled by logging.captureWarnings(True) though.
warnings.simplefilter('default', DeprecationWarning)
        
        
def _resolve_ip_port(nao_id=None, nao_port=None):
    '''
    Return a tuple (ip, port) of detectable or probable NAO.
    The suggested ID can be an IP address, a hostname like bobot.local,
    or a robot name like bobot.
    '''
    if nao_id is None:
        # Ensure consistency. Do not support specifying only port.
        nao_port = None
    else:
        nao_id = str(nao_id)
        
    all_naos = avahi.find_all_naos()
    if nao_port is None:
        if nao_id is not None:
            return _resolve_from_id(all_naos, nao_id)
        else:
            return _find_probable_ip_port(all_naos)
    else:
        # Resolve the ID but discard the port given by Avahi.
        nao_ip, _ = _resolve_from_id(all_naos, nao_id)
        return nao_ip, int(nao_port) 
    
def _resolve_from_id(all_naos, nao_id):
    '''
    Return a tuple (ip, port) corresponding to a robot 'ID'.
    The ID can be an IP address, a hostname like bobot.local,
    or a robot name like bobot.
    '''
    for a_nao in all_naos:
        if nao_id in a_nao.values():
            return a_nao['ip_address'], a_nao['naoqi_port']
    
    # Can't find it in Avahi results.
    # Try with the ID itself and the default port.
    return nao_id, 9559
    
def _find_probable_ip_port(all_naos):
    '''
    Return a tuple (ip, port) likely to be an available NAO around.
    Warning: can do wild guesses.
    '''
    # Prefer to connect to the local naoqi if there is one
    for a_nao in all_naos:
        if a_nao['local']:
            return a_nao['ip_address'], a_nao['naoqi_port']
    
    # No local NAO detected
    if all_naos: # Try to get the first NAO detected by Avahi
        return all_naos[0]['ip_address'], all_naos[0]['naoqi_port']
    else: # Fallback on nao.local/9559
        return 'nao.local', 9559

def _get_local_ip(dest_addr):
    '''
    Return the IP of the *net interface capable of reaching dest_addr.
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((dest_addr, 0))
    ip_addr = sock.getsockname()[0]
    sock.close()
    return ip_addr
    
@contextmanager
def create(broker_name, broker_ip=None, broker_port=0,
           nao_id=None, nao_port=None, **kwargs):
    '''
    Create a broker with the given name.
    Automatically find out NAO IP. Set the broker to listen only on the
    IP that is on the same network than NAO.
    You can specify broker_ip to listen to localhost only (127.0.0.1)
    or to everybody (0.0.0.0).
    
    It acts as a context manager. Which means, use it with the 'with' statement.
    
    Example:
    
    with broker.create('MyBroker') as myBroker:
        print myBroker.getGlobalModuleList()
        raw_input("Press ENTER to terminate the broker")
    # Outside of the with, the broker has been shutdown.
    '''
    broker = Broker(broker_name, broker_ip, broker_port, nao_id, nao_port, **kwargs)
    yield broker
    broker.shutdown()
    
    
class Broker(ALBroker):
    '''
    Create a broker with the given name.
    Automatically find out NAO IP. Set the broker to listen only on the
    IP that is on the same network than NAO.
    You can specify broker_ip to listen to localhost only (127.0.0.1) or
    to everybody (0.0.0.0).
    
    When you are finished with your broker, call the shutdown() method on it.
    '''
    def __init__(self, broker_name, broker_ip=None, broker_port=0,
                 nao_id=None, nao_port=None, **kwargs):
        if any(x in kwargs for x in
                           ['brokerIp', 'brokerPort', 'naoIp', 'naoPort']):
            warnings.warn('''brokerIp, brokerPort, naoIp and naoPort arguments
                             are respectively replaced by broker_ip,
                             broker_port, nao_id and nao_port''',
                             DeprecationWarning)
            broker_ip = kwargs.get('brokerIp', broker_ip)
            broker_port = kwargs.get('brokerPort', broker_port)
            nao_id = kwargs.get('naoIp', nao_id)
            nao_port = kwargs.get('naoPort', nao_port)
                 
        nao_ip, nao_port = _resolve_ip_port(nao_id, nao_port)
        
        # Information concerning our new python broker
        if broker_ip is None:
            broker_ip = _get_local_ip(nao_ip)
      
        ALBroker.__init__(self, broker_name, broker_ip,
                          broker_port, nao_ip, nao_port)
                          
        self.broker_name = broker_name
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.nao_id = nao_id
        self.nao_port = nao_port

