import os
import platform
import json
import datetime
import unittest

from ge_lib.ags.AGSData import get_data, get_all_data, get_data_table, get_df

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
 
class TestAGSTableMethods(unittest.TestCase):
               
    def test_get_data(self):

        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        tables = get_data (ags_file)
        
    def test_get_all_data(self):

        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        tables = get_all_data (ags_file)

    def test_get_data_table(self):
        
        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        tables = get_data_table (ags_file)
    
    
    def test_process(self):
        
        fnames = []

        fnames.append (os.path.join(data_folder,"D1043-21-23122021.ags"))
        fnames.append (os.path.join(data_folder,"21-26216_DETS_16122021_V4.AGS"))
        fnames.append (os.path.join(data_folder, "21-24889_DETS_29112021_V4.AGS"))
        fnames.append (os.path.join(data_folder, "21-25178_DETS_01122021_V4.AGS"))
        fnames.append (os.path.join(data_folder,"21-25179_DETS_01122021_V4.AGS"))

        resp = get_data_table (ags_file)
        