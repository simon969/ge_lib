import os
import platform
import json
import datetime
import unittest

from ge_lib.ags.AGSRules import rules_check


data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
 
class TestAGSChartsMethods(unittest.TestCase):
               
    def test_rules_checkDefault(self):

        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        qry_collection = rules_check (ags_file, "default")
    
    def test_rules_checkLTC(self):

        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        qry_collection = rules_check (ags_file, "LTC")
    
    def test_rules_checkNEOM(self):

        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        qry_collection = rules_check (ags_file, "NEOM")   