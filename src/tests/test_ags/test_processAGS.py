
import os
import platform
import json
import datetime
import unittest

from ge_lib.ags.AGSProcessing import processAGS, ags_group

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
 
class TestAGSSummary(unittest.TestCase):
               
    def test_processAGS(self):

        fnames = []

        fnames.append (os.path.join(data_folder,"D1043-21-23122021.ags"))
        fnames.append (os.path.join(data_folder,"21-26216_DETS_16122021_V4.AGS"))
        fnames.append (os.path.join(data_folder, "21-24889_DETS_29112021_V4.AGS"))
        fnames.append (os.path.join(data_folder, "21-25178_DETS_01122021_V4.AGS"))
        fnames.append (os.path.join(data_folder,"21-25179_DETS_01122021_V4.AGS"))

        ap = processAGS (fnames)
        ap.process()
        ap.report_lines (os.path.join(data_folder, "group_lines.csv"))
        ap.report_summary(os.path.join(data_folder, "point_group_summary.csv"))

if __name__ == '__main__':
    unittest.main()