'''
Created on 4 Apr 2013

@author: dsnowdon
'''

class MockBox(object):
    def __init__(self):
        super(MockBox, self).__init__()

    def log(self, msg):
        print msg

class MockMemory(object):
    def __init__(self):
        super(MockMemory, self).__init__()
        self.values = { }

    def getData(self, name):
        try:
            return self.values[name]
        except KeyError:
            return None
    
    def insertData(self, name, value):
        self.values[name] = value

class MockMotion(object):
    def __init__(self):
        super(MockMotion, self).__init__()
    def getPosition(self, thing, frame, useSensors):
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

class MockTextToSpeech(object):
    def __init__(self):
        super(MockTextToSpeech, self).__init__()
    def getLanguage(self):
        return "English"