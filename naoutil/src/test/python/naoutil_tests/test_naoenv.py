'''
Created on 1 Apr 2013

@author: dsnowdon
'''

import unittest

from naoutil.naoenv import *

class ResourcesPath(unittest.TestCase):
    def test_find_implicit_resources_dir(self):
        env = NaoEnvironment(self, None, None, None)
        rp = env.resources_dir()
        print "Implicit resources path = " + rp
        self.assertNotEqual(None, rp, "Resources path should not be None")

if __name__ == '__main__':
    unittest.main()
