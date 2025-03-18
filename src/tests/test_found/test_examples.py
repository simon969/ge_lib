import os
import unittest


data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","examples")

# https://docs.python.org/3/library/unittest.html

class TestExampleMethods(unittest.TestCase):

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
    def test_to_str(self):
        from ge_lib.found.examples.Examples import FoundExamples
        templates = FoundExamples()
        s = templates.to_str('ground_models_pile_sets.json')
        print (s)

if __name__ == '__main__':
    unittest.main()
   