import os
import platform
import json
import datetime
import unittest

from ge_lib.ags.AGSCharts import get_chart, get_chart_grouped, get_data_chart

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
 
class TestAGSChartsMethods(unittest.TestCase):
               
    def test_get_chart(self):

        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        tables = get_chart (ags_file,[''])
        
    def test_get_chart_grouped(self):

        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        tables = get_chart_grouped (ags_file,[''])

    def test_get_data_chart(self):
        
        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")

        tables = get_data_chart (ags_file,[''])
    