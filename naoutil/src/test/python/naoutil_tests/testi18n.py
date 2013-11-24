# -*- coding: utf8 -*-
'''
Created on Apr 21, 2012

@author: dns
'''
import inspect
import os
import unittest
import tempfile
import shutil

import naoutil.i18n as i18n

class Test(unittest.TestCase):

    def setUp(self):
        self.resources_path = os.path.dirname(inspect.getfile(inspect.currentframe())) + "/../../../../resources"
        # print "reosurces path = " + self.resources_path

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

class TestPropertyFileCache(unittest.TestCase):

    def setUp(self):
        self.resources_path = os.path.dirname(inspect.getfile(inspect.currentframe())) + "/../../../../resources"
        # print "reosurces path = " + self.resources_path

    def tearDown(self):
        pass

    def testReadJsonComesFromCache(self):
        """
        Do an initial read from JSON file, delete the file and verify that property reads still work because
        they are served from the cache
        """
        tmp_json = tempfile.NamedTemporaryFile(mode='w', prefix='example', suffix='_en.json', delete=False)
        fullname = tmp_json.name
        tmp_json.close()
        tmppath = os.path.dirname(fullname)
        name = os.path.basename(fullname)
        prefix = name.replace('_en.json', '')

        # make a copy of a properties file
        copyFile(os.path.join(self.resources_path, 'json_example_en.json'), fullname)

        # read a value from the properties file
        options = i18n.read_text_options(tmppath, prefix, "en", "attractAttention", "/")
        self.assertTrue(options, "attractAttention should be found")
        self.assertTrue(len(options) > 0, "attractAttention should have at least one option")

        # delete the temp file
        os.remove(fullname)

        # check read of different property from same file still works
        options = i18n.read_text_options(tmppath, prefix, "en", "goodbye", "/")
        self.assertTrue(options, "goodbye should be found")
        self.assertTrue(len(options) > 0, "goodbye should have at least one option")

    def testReadPropertiesComesFromCache(self):
        """
        Do an initial read from Java properties file, delete the file and verify that property reads still work because
        they are served from the cache
        """
        tmp_json = tempfile.NamedTemporaryFile(mode='w', prefix='defaults', suffix='_en.properties', delete=False)
        fullname = tmp_json.name
        tmp_json.close()
        tmppath = os.path.dirname(fullname)
        name = os.path.basename(fullname)
        prefix = name.replace('_en.properties', '')

        # make a copy of a properties file
        copyFile(os.path.join(self.resources_path, 'defaults_en.properties'), fullname)

        # read a value from the properties file
        options = i18n.read_text_options(tmppath, prefix, "en", "attractAttention", "/")
        self.assertTrue(options, "attractAttention should be found")
        self.assertTrue(len(options) > 0, "attractAttention should have at least one option")

        # delete the temp file
        os.remove(fullname)

        # check read of different property from same file still works
        value = i18n.get_property(tmppath, prefix, "en", "hello")
        self.assertTrue(len(value), "hello should be found")

    def testRemovingCache(self):
        pass

def copyFile(src, dest):
    try:
        shutil.copy(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
