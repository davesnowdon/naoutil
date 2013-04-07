from naoutil import ALModule
from naoqi import ALProxy

class _SubscriberModule(ALModule):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(_SubscriberModule, cls).__new__(cls, *args, **kwargs)
        return cls._instance
        
    def __init__(self):
        ALModule.__init__(self)
        self.memory = ALProxy('ALMemory')
        self.dataNameToCallback = {}
        
    def subscribeToMicroEvent(self, dataName, callback, cbMessage):
        self.dataNameToCallback[dataName] = callback
        self.memory.subscribeToMicroEvent(dataName, self.moduleName, cbMessage, 'microEventCB')
        
    def unsubscribeToMicroEvent(self, dataName):
        if dataName in self.dataNameToCallback:
            self.memory.unsubscribeToMicroEvent(dataName, self.moduleName)
            del self.dataNameToCallback[dataName]
        
    def microEventCB(self, dataName, value, message):
        self.dataNameToCallback[dataName](dataName, value, message)
        
def subscribeToMicroEvent(dataName, callback, cbMessage):
    _SubscriberModule().subscribeToMicroEvent(dataName, callback, cbMessage)
        
def unsubscribeToMicroEvent(dataName):
    _SubscriberModule().unsubscribeToMicroEvent(dataName)
