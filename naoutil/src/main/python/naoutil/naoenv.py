'''
Created on Feb 10, 2013

@author: dsnowdon

Code used to abstract away some of the details of the NAOqi environment
so that clients do not need to pass around proxies and objects holding
loggers. Instead code justs passes around NaoEnvironment instances
'''

from naoqi import ALProxy

'''
Hold information about the NAO environment and provide abstraction for logging
'''
class NaoEnvironment(object):
    def __init__(self, box_, memory_, motion_, tts_):
        super(NaoEnvironment, self).__init__()
        self.box = box_
        self.memory = memory_
        self.motion = motion_
        self.tts = tts_
    
    def log(self, msg):
        self.box.log(msg)

'''
Create environment object.
Needs to be called from a process with an ALBroker running (for example
within choreographe code)
'''
def make_environment(box_):
    # TODO make proxy handling more general
    return NaoEnvironment(box_,
                          ALProxy("ALMemory"), 
                          ALProxy("ALMotion"), 
                          ALProxy("ALTextToSpeech"))