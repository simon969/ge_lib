import os
import unittest
import time

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
    def test_getSoilResultsSteps(self):

        from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
            
        lst_pnts = ['P01,-0.5,9.95','P02,-1.0,9.95','P03,-2.0,9.95','P04,-4.0,9.95','P05,-8.0,9.95']

        file_out =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\soil_results.csv'
        
        try:
            plx = GetPlaxisResults(host="ukcrdw1rc04g2",
                            port=10000,
                            password='39XW$k32f~h%PTD')
            if plx:
                plx.add_points_list (lst_pnts)
                plx.getSoilResultsByPointsBySteps(fileOut=file_out,
                                        sphaseOrder='Phase_4')
        
        except Exception as e:
            print (str(e))
    
    def test_getInterfaceDynamicByPointsBySteps(self):
        from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
            
        lst_points = ['P01,0.0,10.0','P02,0.0,9.0','P03,0.0,8.0','P04,0.0,7.0','P05,0.0,6.0','P06,0.0,5.0','P07,0.0,4.0','P08,0.0,3.0']
        file_out1 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\interface_results.csv'
        file_out2 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\interface_single_results.csv'

        try:
            plx = GetPlaxisResults(host="ukcrdw1rc04g2",
                            port=10000,
                            password='39XW$k32f~h%PTD')
            if plx:
                plx.add_points_list (lst_points)
                plx.getInterfaceDynamicResultsByPointsBySteps(fileOut=file_out1,
                                        sphaseOrder='Phase_5')
                plx.getInterfaceDynamicSingleResultsByPointsBySteps(fileOut=file_out2,
                                        sphaseOrder='Phase_5')
        
        except Exception as e:
            print (str(e))
    
    def test_getSoilDynamicByPointsBySteps(self):
        from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
            
        lst_nodes = ['P01,0.0,10.0','P02,0.0,9.0','P03,0.0,8.0','P04,0.0,7.0','P05,0.0,6.0','P06,0.0,5.0','P07,0.0,4.0','P08,0.0,3.0']
        file_out =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\soil_results.csv'
        file_out2 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\soil_single_results.csv'
        
        try:
            plx = GetPlaxisResults(host="ukcrdw1rc04g2",
                            port=10000,
                            password='39XW$k32f~h%PTD')
            if plx:
                plx.add_points_list (lst_nodes)
                plx.getSoilDynamicResultsByPointsBySteps(fileOut=file_out,
                                        sphaseOrder='Phase_5')
                plx.getSoilDynamicSingleResultsByPointsBySteps(fileOut=file_out2,
                                        sphaseOrder='Phase_5')
        except Exception as e:
            print (str(e))
    def test_dynamic_task(self):
        from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
            
        lst_nodes = ['P01,0.0,10.0','P02,0.0,9.0','P03,0.0,8.0','P04,0.0,7.0','P05,0.0,6.0','P06,0.0,5.0','P07,0.0,4.0','P08,0.0,3.0']
        file_out =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\interface_results.csv'
        
        try:
            plx = GetPlaxisResults(host="ukcrdw1rc04g2",
                            port=10000,
                            password='39XW$k32f~h%PTD')
            if plx:
                plx.add_points_list (lst_nodes)
                phases = plx.getPhaseList()
                for phase in phases:
                    
                    if phase=='Phase_5':
                        t1 = time.perf_counter()
                        plx.setPhaseOrder(sphaseOrder=phase)
                        plx.setSteps (plx.phaseOrder[0])
                        if plx.Steps:
                            for step in plx.Steps:
                                plx.getInterfaceDynamicResultsByPointsBySteps (
                                                                               steps=[step],
                                                                               fileOut=file_out, 
                                                                               tableOut=None,
                                                                               PhaseName=phase,
                                                                               mode='existing'
                                                                                )    
                        t2 = time.perf_counter()                 
                        print(f"task time {t2 - t1:0.4f} seconds")
        except Exception as e:
            print (str(e)) 

    def test_dynamic_task2(self):
        from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
            
        lst_nodes = ['P01,0.0,10.0','P02,0.0,9.0','P03,0.0,8.0','P04,0.0,7.0','P05,0.0,6.0','P06,0.0,5.0','P07,0.0,4.0','P08,0.0,3.0']
        file_out =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\interface_results.csv'
        
        try:
            plx = GetPlaxisResults(host="ukcrdw1rc04g2",
                            port=10000,
                            password='39XW$k32f~h%PTD')
            if plx:
                plx.add_points_list (lst_nodes)
                phases = plx.getPhaseList()
                for phase in phases:
                    
                    if phase=='Phase_5':
                        t1 = time.perf_counter()
                        plx.setPhaseOrder(sphaseOrder=phase)
                        plx.setSteps (plx.phaseOrder[0])
                        plx.getInterfaceDynamicResultsByPointsBySteps (
                                                                    steps=plx.Steps,
                                                                    fileOut=file_out, 
                                                                    tableOut=None,
                                                                    PhaseName=phase,
                                                                    mode='existing'
                                                                    )    
                        t2 = time.perf_counter()                 
                        print(f"task2 time {t2 - t1:0.4f} seconds")
        except Exception as e:
            print (str(e)) 
    def test_dynamic_single_task(self):
        from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
            
        lst_nodes = ['P01,0.0,10.0','P02,0.0,9.0','P03,0.0,8.0','P04,0.0,7.0','P05,0.0,6.0','P06,0.0,5.0','P07,0.0,4.0','P08,0.0,3.0']
        file_out =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\interface_single_results.csv'
        
        try:
            plx = GetPlaxisResults(host="ukcrdw1rc04g2",
                            port=10000,
                            password='39XW$k32f~h%PTD')
            if plx:
                plx.add_points_list (lst_nodes)
                phases = plx.getPhaseList()
                for phase in phases:
                    
                    if phase=='Phase_5':
                        t1 = time.perf_counter()
                        plx.setPhaseOrder(sphaseOrder=phase)
                        plx.setSteps (plx.phaseOrder[0])
                        if plx.Steps:
                            for step in plx.Steps:
                                plx.getInterfaceDynamicSingleResultsByPointsBySteps (
                                                                               steps=[step],
                                                                               fileOut=file_out, 
                                                                               tableOut=None,
                                                                               PhaseName=phase,
                                                                               mode='existing'
                                                                                )    
                        t2 = time.perf_counter()                 
                        print(f"single_task time {t2 - t1:0.4f} seconds")
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