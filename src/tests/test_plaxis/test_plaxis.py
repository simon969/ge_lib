import os
import unittest

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")

data_folders = {"044":os.path.join(data_folder, "Model 044"),
                "default":os.path.join(data_folder, "default")
                }
class TestGetPlaxisResultsMethods(unittest.TestCase):
     
    def test_getSoilResultsByPoint(self):
        
        from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
        
        file_points = os.path.join(data_folders["044"],"points.csv")
        file_out =  os.path.join(data_folders["044"],"soil_results.csv")
        
        try:
            plx = GetPlaxisResults(host="UKCRD1PC34587",
                            port=10000,
                            password='D@r>Srh1/vft9#ky')
            if plx:
                plx.getSoilResultsByPoints(fileOut=file_out,
                                      filePoints=file_points,
                                      sphaseOrder='Phase_23,Phase_24,Phase_26')
        
        except Exception as e:
            print (str(e))

class TestPlaxis2dConnectV22Methods(unittest.TestCase):
               
    def test_Plaxis2DgetAllStructuralResults(self):
        
        from ge_lib.plaxis.PlaxisResults import Plaxis2dResultsConnectV22
  
        try:
            plx = Plaxis2dResultsConnectV22(host="UKCRD1PC34587",
                            port=10000,
                            password='D@r>Srh1/vft9#ky')
            if plx:
                plx.getAllStructuralResults(folderOut=data_folders["044"], 
                                            sphaseOrder='Phase_23,Phase_24,Phase_26')

        except Exception as e:
            print (str(e))
            
if __name__ == '__main__':
    unittest.main()        