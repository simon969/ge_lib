import os
import unittest
import json
from ge_lib.general.section_props.SectionProperties import SectionProperties 

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","section_properties")

class TestSectionPropMethods(unittest.TestCase):
     
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
    def test_rectangular_section(self):
         
        sp =  SectionProperties()
        
        # 1200 deep x 600 wide beam
        # data unclosed shape
        data = [
                [0,0],
                [0,1.2],
                [0.6,1.2],
                [0.6,0]
                ]
        
        values, symbols, description, units = sp.calc_props(data)
        result_open = {"coords":data,
                       "symbols":symbols,
                       "description":description,
                       "units":units,
                       "values":values} 
        fout = os.path.join(data_folder,"rectangle_open.json")
        json_to_file(fout, result_open)


         # data closed shape
        data = [
                [0,0],
                [0,1.2],
                [0.6,1.2],
                [0.6,0],
                [0,0]
                ]
        values, symbols, description, units = sp.calc_props(data)
        result_closed = {"coords":data,
                         "symbols":symbols,
                         "description":description,
                         "units":units,
                         "values":values} 
        fout = os.path.join(data_folder,"rectangle_closed.json")
        json_to_file(fout, result_closed)
        
        # data closed shape, coords with units
        data = {"coords":[
                [0,0],
                [0,1.2],
                [0.6,1.2],
                [0.6,0],
                [0,0]
                ],
                "units":"m"
                }
        values, symbols, description, units = sp.calc_props(data)
        json_str = json.dumps(result_open)
        print (json_str)

        result_with_units = {"coords":data["coords"],
                             "coord_units":data["units"],
                             "symbols":symbols,
                             "description":description,
                             "units":units,
                             "values":values
                            } 
        fout = os.path.join(data_folder,"rectangle_with_units.json")
        json_to_file(fout, result_with_units)
        
    def test_triangle(self):
        
        # 3m high 2m base right angled triangle
        data = {"coords":[
                [0,0],
                [0,3],
                [2.0,0],
                [0,0]
                ],
                "units":"m"}
        
        sp =  SectionProperties()

        values, symbols, description, units = sp.calc_props(data)
        result = {"data":data,
                    "symbols":symbols,
                    "description":description,
                    "units": units,
                    "values":values} 
        fout = os.path.join(data_folder,"triangle.json")
        json_to_file(fout, result)
    def test_isection(self):

        # 356 x 406 x 634 x 633.9kg/m UC
        data = {"name":"356x406x634x633.9kg/m",
                "coords":[
                            [0,0],
                            [0,77],
                            [188.2,77],
                            [188.2,397.6],
                            [0,397.6],
                            [0,474.6],
                            [424,474.6],
                            [424,397.6],
                            [235.8,397.6],
                            [235.8,77],
                            [424,77],
                            [424,0],
                            [0,0]],
                "units":"mm"}

        
        sp =  SectionProperties()

        values, symbols, description, units = sp.calc_props(data)
        result = {"data":data,
                    "symbols":symbols,
                    "description":description,
                    "units": units,
                    "values":values} 
        fout = os.path.join(data_folder,"isection.json")
        json_to_file(fout, result)
        print (result)

def json_to_file(fname, data):
    
    if type(data) is list:
        json_string = json.dumps([ob.__dict__ for ob in data])
    else:
        json_string = json.dumps(data)
    
    with open(fname, 'w') as f:
       f.write (json_string)
    print('Output written to ' + fname)


if __name__ == '__main__':
    unittest.main()
