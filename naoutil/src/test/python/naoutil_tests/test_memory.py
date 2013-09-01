'''
Created on August 31, 2013

@author: AxelVoitier
@license: GNU LGPL v3

Test suite for naoutil.broker module.
'''
import __main__
import unittest

import naoqi

from naoutil.general import singleton

class FakeALModule(object):
    def __init__(self, *args):
        pass

@singleton
class FakeALMemoryProxy(object):
    def __init__(self, *args):
        self.event_callbacks = {}
        self.micro_event_callbacks = {}
        
    def subscribeToEvent(self, data_name, module_name, callback_name):
        self.event_callbacks[data_name] = (module_name, callback_name)
        
    def unsubscribeToEvent(self, data_name, module_name):
        if data_name in self.event_callbacks:
            del self.event_callbacks[data_name]
            
    def raise_event(self, data_name, value):
        if data_name in self.event_callbacks:
            module = getattr(__main__, self.event_callbacks[data_name][0])
            callback = getattr(module, self.event_callbacks[data_name][1])
            callback(data_name, value, '')
        
    def subscribeToMicroEvent(self, data_name, module_name, message, callback_name):
        self.micro_event_callbacks[data_name] = (module_name, callback_name, message)
        
    def unsubscribeToMicroEvent(self, data_name, module_name):
        if data_name in self.micro_event_callbacks:
            del self.micro_event_callbacks[data_name]
            
    def raise_micro_event(self, data_name, value):
        if data_name in self.micro_event_callbacks:
            module = getattr(__main__, self.micro_event_callbacks[data_name][0])
            callback = getattr(module, self.micro_event_callbacks[data_name][1])
            callback(data_name, value, self.micro_event_callbacks[data_name][2])

class MemoryCallback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        naoqi.ALModule = FakeALModule
        naoqi.ALProxy = FakeALMemoryProxy
    
    @classmethod
    def tearDownClass(cls):
        reload(naoqi)
        
    def test_event(self):
        from naoutil import memory
        events = {'data1': [1234, None], 'data2': [5678, None]}
        def my_callback(data_name, value, message):
            events[data_name][1] = value
            self.assertEqual(value, events['data1'][0])
            
        memory.subscribe_to_event('data1', my_callback)
        memory.subscribe_to_event('data2', my_callback)
        FakeALMemoryProxy().raise_event('data1', events['data1'][0])
        self.assertIsNotNone(events['data1'][1])
        self.assertIsNone(events['data2'][1])
        
        memory.unsubscribe_to_event('data2')
        events['data1'][1] = None
        FakeALMemoryProxy().raise_event('data2', events['data2'][0])
        self.assertIsNone(events['data2'][1])
        self.assertIsNone(events['data1'][1])
        
        memory.unsubscribe_to_event('data1')
        
    def test_micro_event(self):
        from naoutil import memory
        events = {'data1': [1234, 'msg2', None, None], 'data2': [5678, 'msg2', None, None]}
        def my_callback(data_name, value, message):
            events[data_name][2] = value
            events[data_name][3] = message
            self.assertEqual(value, events['data1'][0])
            self.assertEqual(message, events['data1'][1])
            
        memory.subscribe_to_micro_event('data1', my_callback, events['data1'][1])
        memory.subscribe_to_micro_event('data2', my_callback, events['data2'][1])
        FakeALMemoryProxy().raise_micro_event('data1', events['data1'][0])
        self.assertIsNotNone(events['data1'][2])
        self.assertIsNone(events['data2'][2])
        self.assertIsNotNone(events['data1'][3])
        self.assertIsNone(events['data2'][3])
        
        memory.unsubscribe_to_micro_event('data2')
        events['data1'][2] = None
        events['data1'][3] = None
        FakeALMemoryProxy().raise_micro_event('data2', events['data2'][0])
        self.assertIsNone(events['data2'][2])
        self.assertIsNone(events['data1'][2])
        self.assertIsNone(events['data2'][3])
        self.assertIsNone(events['data1'][3])
        
        memory.unsubscribe_to_micro_event('data1')

if __name__ == '__main__':
    unittest.main()
