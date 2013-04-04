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
The short names are the ones used to generate python properties, so you can use env.tts instead of
env.ALTextToSpeech
'''
PROXY_SHORT_NAMES = { 'audioDevice' : 'ALAudioDevice',
                      'audioLocalisation' : 'ALAudioSourceLocalisation',
                      'audioPlayer' : 'ALAudioPlayer',
                      'audioRecorder' : 'ALAudioRecoder',
                      'behaviourManager' : 'ALBehaviorManager',
                      'connectionManager' : 'ALConnectionManager',
                      'faceDetection' : 'ALFaceDetection',
                      'infrared' : 'ALInfrared',
                      'leds' : 'ALLeds',
                      'memory' : 'ALMemory',
                      'motion' : 'ALMotion',
                      'navigation' : 'ALNavigation',
                      'photoCapture' : 'ALPhotoCapture',
                      'preferences' : 'ALPreferences',
                      'resourceManager' : 'ALResourceManager',
                      'robotPosture' : 'ALRobotPosture',
                      'sensors' : 'ALSensors',
                      'sonar' : 'ALSonar',
                      'soundDetection' : 'ALSoundDetection',
                      'speechRecognition' : 'ALSpeechRecognition',
                      'tts' : 'ALTextToSpeech',
                      'videoDevice' : 'ALVideoDevice',
                      'videoRecorder' : 'ALVideoRecorder',
                      'visionRecognition' : 'ALVisionRecognition' }

'''
Hold information about the NAO environment and provide abstraction for logging
'''
# TODO build proxies on demand using python properties with custom getter
class NaoEnvironment(object):
    def __init__(self, box_, proxies_={}):
        super(NaoEnvironment, self).__init__()
        self.box = box_
        self.resources_path = None
        # construct the set of proxies, ensuring that we use only valid long names
        self.proxies = { }
        longNames = PROXY_SHORT_NAMES.values()
        for n, v in proxies_.iteritems():
            if n in longNames:
                self.proxies[n] = v
            elif n in PROXY_SHORT_NAMES:
                self.proxies[PROXY_SHORT_NAMES[n]] = v
    
    def log(self, msg):
        self.box.log(msg)
    
    def resources_dir(self):
        if self.resources_path is None:
            # if a path has not been set explicitly then find this path and replace everything
            # from src downwards with resources
            this_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            prefix_end_index = this_dir.rindex(SOURCE_DIR)
            prefix = this_dir[0:prefix_end_index]
            self.resources_path = prefix + RESOURCE_DIR
        
        return self.resources_path
    
    def set_resources_dir(self, dir_name):
        self.resources_path = dir_name
    
    def current_language(self):
        return self.tts.getLanguage()
    
    # return the two letter ISO language code for the current language
    def current_language_code(self):
        return i18n.language_to_code(self.current_language())
    
    def localized_text(self, basename, property_name):
        language_code = self.current_language_code()
        lt = i18n.get_property(self.resources_dir(), 
                               basename, 
                               language_code, 
                               property_name)
        self.log("Property '"+property_name+"' resolved to text '"+lt+"' in language '"+language_code+"'")
        return lt

    # simulate having properties for all proxies without having to manually create each one
    def __getattr__(self, name):
        if name in PROXY_SHORT_NAMES or name in PROXY_SHORT_NAMES.values():
            # get the correct long name (key)
            key = name
            if name in PROXY_SHORT_NAMES:
                key = PROXY_SHORT_NAMES[name]
            
            if not key in self.proxies:
                self.add_proxy(key)
            
            return self.proxies[key]
        else:
            # not a valid short name or long name
            raise AttributeError

    # invoke ALProxy to create the proxy we need
    def add_proxy(self, longName):
        self.log('Creating proxy: ' + longName)
        self.proxies[longName] = ALProxy(longName)

'''
Create environment object.
Needs to be called from a process with an ALBroker running (for example
within choreographe code)
'''
def make_environment(box_):
    return NaoEnvironment(box_, {})