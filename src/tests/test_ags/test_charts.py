import os
import platform
import json
import datetime
import unittest

from ge_lib.ags.AGSCharts import get_chart, get_chart_grouped, get_data_chart
from ge_lib.ags.AGSData import get_data
data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
 
class TestAGSChartsMethods(unittest.TestCase):
               
    def test_get_chart(self):

        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")
        df = get_data (ags_file)
        if df:
            charts = get_chart (df,table='ISPT')
        
    def test_get_chart_grouped(self):

        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")
        df = get_data (ags_file)
        if df:
            charts = get_chart_grouped (df, table='ISPT')

    def test_get_data_chart(self):
        
        ags_file = os.path.join(data_folder,"D1043-21-23122021.ags")
        df = get_data (ags_file)
        if df:
            charts = get_data_chart (ags_file,tables=None,table='ISPT')
    
    def test_process (self):
        fnames = []
        errors = []
        fnames.append (os.path.join(data_folder,"D1043-21-23122021.ags"))
        fnames.append (os.path.join(data_folder,"21-26216_DETS_16122021_V4.AGS"))
        fnames.append (os.path.join(data_folder, "21-24889_DETS_29112021_V4.AGS"))
        fnames.append (os.path.join(data_folder, "21-25178_DETS_01122021_V4.AGS"))
        fnames.append (os.path.join(data_folder,"21-25179_DETS_01122021_V4.AGS"))
        df = get_data(fnames)
        if df:
            charts = get_data_chart (df,tables=None,table='ISPT')

if __name__ == '__main__':
    unittest.main()