# -*- coding: utf8 -*-
'''
Created on Apr 21, 2012

@author: dns
'''
import inspect
import os
import unittest

import naoutil.i18n as i18n

class Test(unittest.TestCase):


    def setUp(self):
        self.resources_path = os.path.dirname(inspect.getfile(inspect.currentframe())) + "/../../../../resources"
        #print "reosurces path = " + self.resources_path

    def tearDown(self):
        pass


    def testLanguageCode(self):
        self.assertEquals("zh", i18n.language_to_code("Chinese"))
        self.assertEquals("en", i18n.language_to_code("English"))
        self.assertEquals("fr", i18n.language_to_code("French"))
        self.assertEquals("de", i18n.language_to_code("German"))
        self.assertEquals("it", i18n.language_to_code("Italian"))
        self.assertEquals("ja", i18n.language_to_code("Japanese"))
        self.assertEquals("ko", i18n.language_to_code("Korean"))
        self.assertEquals("es", i18n.language_to_code("Spanish"))

    def testLoadPropertiesEnglish(self):
        hello_value = i18n.get_property(self.resources_path, "defaults", "en", "hello")
        self.assertEquals("Hello", hello_value)
    
    def testLoadPropertiesFrench(self):
        hello_value = i18n.get_property(self.resources_path, "defaults", "fr", "hello")
        self.assertEquals("Bonjour", hello_value)
    
    def testLoadPropertiesChinese(self):
        hello_value = i18n.get_property(self.resources_path, "defaults", "zh", "hello")
        self.assertEquals("你好", hello_value)
    
    def testLoadOptionsTextFileEnglish(self):
        options = i18n.read_text_options(self.resources_path, "example", "en")
        self.assertEqual(5, len(options))
    
    def testLoadOptionsTextFileFrench(self):
        options = i18n.read_text_options(self.resources_path, "example", "fr")
        self.assertEqual(5, len(options))

    def testLoadOptionsTextFileChinese(self):
        options = i18n.read_text_options(self.resources_path, "example", "zh")
        self.assertEqual(5, len(options))
    
    def testLoadOptionsPropertyFileEnglish(self):
        options = i18n.read_text_options(self.resources_path, "defaults", "en", "attractAttention", "/")
        self.assertEqual(5, len(options))

    def testLoadOptionsPropertyFileFrench(self):
        options = i18n.read_text_options(self.resources_path, "defaults", "fr", "attractAttention", "/")
        self.assertEqual(5, len(options))
    
    def testLoadOptionsPropertyFileChinese(self):
        options = i18n.read_text_options(self.resources_path, "defaults", "zh", "attractAttention", "/")
        self.assertEqual(5, len(options))
    
    # should not need to do anything different, the library should automatically load the JSON
    def testLoadOptionsJsonFileEnglish(self):
        options = i18n.read_text_options(self.resources_path, "json_example", "en", "attractAttention", "/")
        self.assertEqual(5, len(options))

    def testLoadOptionsJsonFileFrench(self):
        options = i18n.read_text_options(self.resources_path, "json_example", "fr", "attractAttention", "/")
        self.assertEqual(5, len(options))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()