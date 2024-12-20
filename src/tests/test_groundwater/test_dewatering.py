import os
import unittest
import json
from ge_lib.groundwater.dewatering import DewateringSite 

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","section_properties")

class TestDewateringMethods(unittest.TestCase):
     
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)