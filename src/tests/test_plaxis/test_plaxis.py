import os
import unittest

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","examples")


class TestGetPlaxisResultsMethods(unittest.TestCase):
     
    def test_getSoilResultsByPoint(self):
        
        from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
        
        try:
            plx = GetPlaxisResults(host="UKCRD1nnn",
                            port=10000,
                            password='')
        
            plx.getSoilResultsByPoint(folderOut=data_folder)
        
        except ConnectionError:
            print ("Connection Error")
        # except MaxRetryError:
            # print ("Max Retry Error")    
        except Exception as e:
            print (str(e))

class TestPlaxis2dConnectV22Methods(unittest.TestCase):
               
    def test_Plaxis2DgetSoilResultsByPoint(self):
        
        from ge_lib.plaxis.PlaxisResults import Plaxis2dResultsConnectV22

        try:
            plx = Plaxis2dResultsConnectV22(host="UKCRD1nnn",
                            port=10000,
                            password='')
        
            plx.getAllStructuralResults(folderOut=data_folder)
        
        except ConnectionError:
            print ("Connection Error")
        except Exception as e:
            print (str(e))
        