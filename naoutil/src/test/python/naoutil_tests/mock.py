'''
Created on 4 Apr 2013

@author: dsnowdon
'''

class MockBox(object):
    def __init__(self):
        super(MockBox, self).__init__()

    def log(self, msg):
        print msg
