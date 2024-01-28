import unittest
import platform
import json
from src.ge_lib.found.pyGround.GroundModel import GroundModel
from src.ge_lib.found.pyGround.GroundStresses import GroundStresses
from src.ge_lib.found.pyPile.PileGeoms import CircularPile
from src.ge_lib.found.pyPile.PileResistances import PileResistance
from src.ge_lib.found.pyPile.EC7PartialFactors import get_factors
from .test_ground import getGroundModel
from .test_support import json_to_file, csv_to_file

if (platform.system()=='Linux'):
    temp_path ='/mnt/chromeos/GoogleDrive/MyDrive/Projects/tests/examples/'    
else:
    temp_path = 'G:\\My Drive\\Projects\\examples\\'

# https://docs.python.org/3/library/unittest.html

class TestStringMethods(unittest.TestCase):

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

    def test_SaveRetrieveExample101(self):
        
        gm = getGroundModel ('101')
                
        json_text1 = gm.to_json()
        json_to_file (temp_path + "gm.json", json_text1)

        f = open(temp_path + "gm.json")
        data = json.load(f)
        f.close()
        try :
            gm2 = GroundModel(data)
            json_text2 = gm2.to_json()
            self.assertEqual(json_text1, json_text2)
        except Exception as e:
            print (str(e))

    def test_ResistanceExample101(self):
        
        gm = getGroundModel ('101')
        gm.collectStrataSet (['_default'])
        gs = GroundStresses ("Groundmodel sampled from +102m to +42m in -0.5m steps", gm, 102, 42, -0.5)
        res_stress = gs.getStresses ();
        json_to_file (temp_path + 'res_stress.csv', res_stress)    
        
        cp = CircularPile ( "CFA_450", dia=0.45,alpha= 0.6,ks=0.8,tan_delta=0.67, nq=200)
        
        pr = PileResistance ("Groundmodel sampled from +102m to +42m in -0.5m steps", cp, gm, 102, 42, -0.5)
      
        res_sls = pr.getResistances (get_factors("unity_factors"))
        res_uls_c1 = pr.getResistances (get_factors("uls_c1_cfa_factors"))
        res_uls_c2 = pr.getResistances (get_factors("uls_c2_cfa_factors"))
        
        json_to_file ( temp_path + "res_sls.json", res_sls)
        json_to_file ( temp_path + "res_uls_c1.json", res_uls_c1)
        json_to_file ( temp_path + "res_uls_c2.json", res_uls_c2)


    


if __name__ == '__main__':
    unittest.main()