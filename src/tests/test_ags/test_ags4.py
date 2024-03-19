import os
import platform
import json
import datetime
import unittest

from ge_lib.ags.AGSWorkingGroup import check_file, export_xlsx

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")

    
class TestAGS4Methods(unittest.TestCase):
               
    def test_ags_check(self):
       
        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")
        dict_file  = os.path.join(data_folder,"D1043-21-23122021.ags")
        checks_bytes = check_file (ags_file,dict_file)
        

    def test_export_xlsx(self):
        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")
        xlsx_file_bytes  = export_xlsx(ags_file)

if __name__ == '__main__':
    unittest.main()    