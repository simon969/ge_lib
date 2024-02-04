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

        tables = get_data (ags_file,[''])
        
    def test_get_all_data(self):

        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        tables = get_all_data (ags_file,[''])

    def test_get_data_table(self):
        
        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        tables = get_data_table (ags_file,[''])
    
    def test_get_df(self):
        
        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        tables = get_df (ags_file,[''])
   