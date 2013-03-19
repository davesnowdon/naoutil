'''
Created on Feb 19, 2013

@author: dsnowdon
'''

import unittest

from naoutil.general import *

'''
Test free functions in general utilities
'''
class TestFreeFunctions(unittest.TestCase):
    def test_fqcn_to_module(self):
        self.assertEqual(FQCN_to_module("naoutil_tests.test_jsonobj.JsonTestBase"), "naoutil_tests.test_jsonobj")

    def test_fqcn_to_module_no_module(self):
        self.assertIsNone(FQCN_to_module("Start")) 

    def test_fqcn_to_class(self):
        self.assertEqual(FQCN_to_class("naoutil_tests.test_jsonobj.JsonTestBase"), "JsonTestBase")

    def test_fqcn_to_class_no_module(self):
        self.assertEqual(FQCN_to_class("Start"), "Start")

    def test_find_class(self):
        self.assertIsNotNone(find_class('naoutil_tests.test_jsonobj.JsonTestBase'))


if __name__ == '__main__':
    unittest.main()