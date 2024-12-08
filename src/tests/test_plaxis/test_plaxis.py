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
        
        # 2d model parameters
        # pnt_lst = ['P01,0.0,10.0','P02,0.0,9.0','P03,0.0,8.0','P04,0.0,7.0','P05,0.0,6.0','P06,0.0,5.0','P07,0.0,4.0','P08,0.0,3.0']
        # password = '39XW$k32f~h%PTD'
        # host = "ukcrdw1rc04g2"
        # port=10000
        # file_out1 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\interface_results.csv'
        # file_out2 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\interface_single_results.csv'
        # phases =['Phase_5']
        
        #3d model parameters
        # pnt_lst = ['P01,0.0,0.0,0.0','P02,0.5,0.0,0.0','P03,0.0,0.5,0.0','P04,0.0,0.5,0.5','P05,0.0,1.0,1.0','P06,0.0,2.0,2.0','P07,0.0,3.0,3.0','P08,0.0,4.0,4.0']
        pnt_lst = self.get_plaxis3d_nodes()
        host = "ukcrdw1rc04g2"
        password = 'HL%7<c1SYNwXi?Ww' 
        port = 10000
        file_out1 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\interface_results3d_v2.csv'
        # file_out2 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\interface_single_results3d.csv'
        phases = ['Phase_3']
        file_out2 = None
        
        self.getInterfaceDynamicByPointsBySteps (host=host,
                                                 port=port,
                                                 password=password,
                                                 pnt_lst = pnt_lst,
                                                 phases=phases,
                                                 file_out = file_out1,
                                                 single_file_out = file_out2
                                                 )
    def test_getSoilDynamicByPointsBySteps(self):
        
        # 2d model parameters
        # pnt_lst = ['P01,0.0,10.0','P02,0.0,9.0','P03,0.0,8.0','P04,0.0,7.0','P05,0.0,6.0','P06,0.0,5.0','P07,0.0,4.0','P08,0.0,3.0']
        # password = '39XW$k32f~h%PTD'
        # host = "ukcrdw1rc04g2"
        # port=10000
        # phases = ['Phase_5']
        # file_out1 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\soil_results.csv'
        # file_out2 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\soil_single_results.csv'
        
        #3d model parameters
        # pnt_lst = ['P01,0.0,0.0,0.0','P02,0.5,0.0,0.0','P03,0.0,0.5,0.0','P04,0.0,0.5,0.5','P05,0.0,1.0,1.0','P06,0.0,2.0,2.0','P07,0.0,3.0,3.0','P08,0.0,4.0,4.0']
        pnt_lst = self.get_plaxis3d_nodes()
        host = "ukcrdw1rc04g2"
        password = 'HL%7<c1SYNwXi?Ww' 
        port = 10000
        file_out1 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\soil_results3d.csv'
        file_out2 =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\soil_single_results3d.csv'
        phases = ['Phase_3']
        file_out2 = None

        self.getSoilDynamicByPointsBySteps (host=host,
                                                 port=port,
                                                 password=password,
                                                 pnt_lst = pnt_lst,
                                                 phases=phases,
                                                 file_out = file_out1,
                                                 single_file_out = file_out2
                                                 )    
    def getInterfaceDynamicByPointsBySteps(self, host, port, password, pnt_lst, phases, file_out, single_file_out=None ):

        from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
            
        try:
            plx = GetPlaxisResults(host=host,
                            port=port,
                            password=password)
            if plx:
                plx.add_points_list (pnt_lst) 
                mode = 'new'
                for phase in phases: 
                    plx.setPhaseOrder(sphaseOrder=phase)
                    plx.setSteps (plx.phaseOrder[0])
                    if plx.Steps:
                        for step in plx.Steps:
                            plx.getInterfaceDynamicResultsByPointsBySteps(fileOut=file_out,
                                                                        PhaseName=phase,
                                                                        steps = [step],
                                                                        mode=mode)
                            if single_file_out:
                                plx.getInterfaceDynamicSingleResultsByPointsBySteps(fileOut=single_file_out,
                                                                                PhaseName=phase,
                                                                                steps = [step],
                                                                                mode = mode)
                            mode='existing'
        except Exception as e:
            print (str(e))
    
    def getSoilDynamicByPointsBySteps(self, host, port, password, pnt_lst, phases, file_out, single_file_out=None ):
        from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
            
        try:
            plx = GetPlaxisResults(host=host,
                            port=port,
                            password=password,
                            )
            if plx:
                plx.add_points_list (pnt_lst) 
                mode='new'
                for phase in phases:
                    plx.setPhaseOrder(sphaseOrder=phase)
                    plx.setSteps (plx.phaseOrder[0])
                    if plx.Steps:
                        for step in plx.Steps:
                            plx.getSoilDynamicResultsByPointsBySteps(fileOut=file_out,
                                                                    PhaseName=phase,
                                                                    steps=[step],
                                                                    mode=mode
                                                                    )
                            if single_file_out:
                                plx.getSoilDynamicSingleResultsByPointsBySteps(fileOut=single_file_out,
                                                                            PhaseName=phase,
                                                                            steps=[step],
                                                                            mode=mode)
                            mode='existing'
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
    def get_plaxis3d_nodes(self):
        return ['N4,0.500,0.000,0.000',
                'N6,0.000,0.000,0.000',
                'N12,0.000,0.500,0.000',
                'N14,0.500,0.500,0.000',
                'N95,0.375,0.000,0.000',
                'N97,0.250,0.000,0.000',
                'N99,0.125,0.000,0.000',
                'N101,0.438,0.000,0.000',
                'N103,0.313,0.000,0.000',
                'N105,0.188,0.000,0.000',
                'N107,0.063,0.000,0.000',
                'N281,0.125,0.500,0.000',
                'N283,0.250,0.500,0.000',
                'N285,0.375,0.500,0.000',
                'N287,0.063,0.500,0.000',
                'N289,0.188,0.500,0.000',
                'N291,0.313,0.500,0.000',
                'N293,0.438,0.500,0.000',
                'N295,0.500,0.375,0.000',
                'N297,0.500,0.250,0.000',
                'N299,0.500,0.125,0.000',
                'N301,0.500,0.438,0.000',
                'N303,0.500,0.313,0.000',
                'N305,0.500,0.188,0.000',
                'N307,0.500,0.063,0.000',
                'N309,0.000,0.125,0.000',
                'N311,0.000,0.250,0.000',
                'N313,0.000,0.375,0.000',
                'N315,0.000,0.063,0.000',
                'N317,0.000,0.188,0.000',
                'N319,0.000,0.313,0.000',
                'N321,0.000,0.438,0.000',
                'N2382,0.106,0.192,0.000',
                'N2384,0.313,0.108,0.000',
                'N2386,0.397,0.315,0.000',
                'N2388,0.189,0.399,0.000',
                'N2390,0.313,0.400,0.000',
                'N2392,0.251,0.252,0.000',
                'N2394,0.395,0.190,0.000',
                'N2396,0.188,0.100,0.000',
                'N2398,0.103,0.313,0.000',
                'N2400,0.091,0.409,0.000',
                'N2402,0.409,0.409,0.000',
                'N2404,0.409,0.091,0.000',
                'N2406,0.091,0.091,0.000',
                'N2408,0.455,0.045,0.000',
                'N2410,0.392,0.045,0.000',
                'N2412,0.455,0.108,0.000',
                'N2414,0.108,0.045,0.000',
                'N2416,0.045,0.045,0.000',
                'N2418,0.045,0.108,0.000',
                'N2420,0.045,0.455,0.000',
                'N2422,0.108,0.455,0.000',
                'N2424,0.045,0.392,0.000',
                'N2426,0.392,0.455,0.000',
                'N2428,0.455,0.455,0.000',
                'N2430,0.455,0.392,0.000',
                'N2432,0.344,0.054,0.000',
                'N2434,0.281,0.054,0.000',
                'N2436,0.361,0.100,0.000',
                'N2438,0.219,0.050,0.000',
                'N2440,0.156,0.050,0.000',
                'N2442,0.250,0.104,0.000',
                'N2444,0.139,0.095,0.000',
                'N2446,0.157,0.449,0.000',
                'N2448,0.220,0.449,0.000',
                'N2450,0.140,0.404,0.000',
                'N2452,0.281,0.450,0.000',
                'N2454,0.344,0.450,0.000',
                'N2456,0.251,0.399,0.000',
                'N2458,0.361,0.405,0.000',
                'N2460,0.448,0.345,0.000',
                'N2462,0.448,0.283,0.000',
                'N2464,0.403,0.362,0.000',
                'N2466,0.447,0.220,0.000',
                'N2468,0.447,0.158,0.000',
                'N2470,0.396,0.253,0.000',
                'N2472,0.402,0.141,0.000',
                'N2474,0.053,0.158,0.000',
                'N2476,0.053,0.221,0.000',
                'N2478,0.098,0.141,0.000',
                'N2480,0.052,0.281,0.000',
                'N2482,0.052,0.344,0.000',
                'N2484,0.105,0.252,0.000',
                'N2486,0.097,0.361,0.000',
                'N2488,0.178,0.222,0.000',
                'N2490,0.147,0.146,0.000',
                'N2492,0.219,0.176,0.000',
                'N2494,0.177,0.282,0.000',
                'N2496,0.282,0.180,0.000',
                'N2498,0.354,0.149,0.000',
                'N2500,0.323,0.221,0.000',
                'N2502,0.355,0.358,0.000',
                'N2504,0.282,0.326,0.000',
                'N2506,0.324,0.284,0.000',
                'N2508,0.220,0.325,0.000',
                'N2510,0.146,0.356,0.000']
               
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