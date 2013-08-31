'''
Created on April 06, 2013

@author: AxelVoitier
@license: GNU LGPL v3

Provide helper functions to easilly subscribe to ALMemory
events and micro events.
'''

import weakref

from naoqi import ALProxy

from naoutil import ALModule

def _singleton(cls):
    '''
    Decorator for a class to transform it as a singleton.
    '''
    instances = weakref.WeakValueDictionary()
    def getinstance():
        '''
        Lookup for the class in the weak dict and return its singleton instance.
        Called when creating an object.
        '''
        try:
            return instances[cls]
        except KeyError:
            instances[cls] = cls()
            return instances[cls]
    return getinstance


@_singleton
class _SubscriberModule(ALModule):
    '''
    Singleton ALModule used to subscribe to events and micro-events.
    Not made to be used by a user.
    Prefer to call the module functions.
    '''
    def __init__(self):
        ALModule.__init__(self)
        self.memory = ALProxy('ALMemory')
        self.data_name_to_micro_event_cb = {}
        self.data_name_to_event_cb = {}
        
    # Event
    def subscribe_to_event(self, data_name, callback):
        '''
        Relay the subscription to ALMemory.
        Keep trace of the (data_name, callback) association.
        '''
        self.data_name_to_event_cb[data_name] = callback
        self.memory.subscribe_to_event(data_name, self.module_name, '_event_cb')
        
    def unsubscribe_to_event(self, data_name):
        '''
        Relay the unsubscription to ALMemory.
        Remove reference to the (data_name, callback) association.
        '''
        if data_name in self.data_name_to_event_cb:
            self.memory.unsubscribe_to_event(data_name, self.module_name)
            del self.data_name_to_event_cb[data_name]
        
    def _event_cb(self, data_name, value, message):
        '''
        Callback called by ALMemory when a value change on one of the
        subscribed data_name.
        Relay to user callback.
        '''
        self.data_name_to_event_cb[data_name](data_name, value, message)
        
    # Micro-event
    def subscribe_to_micro_event(self, data_name, callback, cb_message):
        '''
        Relay the subscription to ALMemory.
        Keep trace of the (data_name, callback) association.
        '''
        self.data_name_to_micro_event_cb[data_name] = callback
        self.memory.subscribe_to_micro_event(data_name, self.module_name,
                                             cb_message, '_micro_event_cb')
        
    def unsubscribe_to_micro_event(self, data_name):
        '''
        Relay the unsubscription to ALMemory.
        Remove reference to the (data_name, callback) association.
        '''
        if data_name in self.data_name_to_micro_event_cb:
            self.memory.unsubscribe_to_micro_event(data_name, self.module_name)
            del self.data_name_to_micro_event_cb[data_name]
        
    def _micro_event_cb(self, data_name, value, message):
        '''
        Callback called by ALMemory when a value change on one of the
        subscribed data_name.
        Relay to user callback.
        '''
        self.data_name_to_micro_event_cb[data_name](data_name, value, message)
        
def subscribe_to_event(data_name, callback):
    '''
    Subscribe to an event.
    '''
    _SubscriberModule().subscribe_to_event(data_name, callback)
        
def unsubscribe_to_event(data_name):
    '''
    Unsubscribe to an event.
    '''
    _SubscriberModule().unsubscribe_to_event(data_name)
        
def subscribe_to_micro_event(data_name, callback, cb_message=''):
    '''
    Subscribe to a micro-event.
    '''
    _SubscriberModule().subscribe_to_micro_event(data_name, callback,
                                                 cb_message)
        
def unsubscribe_to_micro_event(data_name):
    '''
    Unsubscribe to an event.
    '''
    _SubscriberModule().unsubscribe_to_micro_event(data_name)
