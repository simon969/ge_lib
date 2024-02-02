import os
import platform
import json
import datetime
import unittest

from ge_lib.ags.AGS4_fs import check_file, AGS4_to_excel

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")

def main ():
    # RunExample101()
    # TestInitData()
    # test_process_request()
    print ("test_pile : main complete(0)".format(datetime.now()))

    
class TestAGS4Methods(unittest.TestCase):
               
    def test_ags_check(self):
       
        print (data_folder)
        