'''
Created on Feb 10, 2013

@author: dsnowdon

Code used to abstract away some of the details of the NAOqi environment
so that clients do not need to pass around proxies and objects holding
loggers. Instead code justs passes around NaoEnvironment instances
'''
import inspect
import os

from naoqi import ALProxy

import i18n

SOURCE_DIR = "src"
RESOURCE_DIR = "resources"

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
        self.resources_path = None
    
    def log(self, msg):
        self.box.log(msg)
    
    def resources_dir(self):
        if self.resources_path is None:
            # if a path has not been set explicitly then find this path and replace everything
            # from src downwards with resources
            this_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            prefix_end_index = this_dir.rindex(SOURCE_DIR)
            prefix = this_dir[0:prefix_end_index]
            return prefix + RESOURCE_DIR
        else:
            return self.resources_path
    
    def set_resources_dir(self, dir_name):
        self.resources_path = dir_name
    
    def current_language(self):
        return self.tts.getLanguage()
    
    # return the two letter ISO language code for the current language
    def current_language_code(self):
        return i18n.language_to_code(self.current_language())
    
    def localized_text(self, basename, property_name):
        return i18n.get_property(self.resources_dir(), 
                                 basename, 
                                 self.current_language_code(), 
                                 property_name)

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