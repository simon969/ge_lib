
def main():

    test_getSoilResultsSteps()



def test_getAllStructuralResults():
    from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
    
    try:
        plx = GetPlaxisResults(host="UKCRD1PC34587",
                        port=10000,
                        password='D@r>Srh1/vft9#ky')
        if plx:
            plx.getAllStructuralResults(folderOut="c:\\Temp", 
                                        sphaseOrder='Phase_23,Phase_24,Phase_26')

    except Exception as e:
        print (str(e))

def test_getAllStructuralResultsV22():
    from ge_lib.plaxis.PlaxisResults import Plaxis2dResultsConnectV22
    
    try:
        plx = Plaxis2dResultsConnectV22(host="UKCRD1PC34587",
                        port=10000,
                        password='D@r>Srh1/vft9#ky')
        if plx:
            plx.getAllStructuralResults(folderOut="c:\\Temp", 
                                        sphaseOrder='Phase_23,Phase_24,Phase_26')

    except Exception as e:
        print (str(e))

def test_getSoilResults():

    from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
        
    file_points = r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\myapp\points.csv'
    file_out =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\myapp\soil_results.csv'
    
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
def test_getSoilResultsSteps():

    from ge_lib.plaxis.PlaxisResults import GetPlaxisResults
        
    lst_pnts = ['P01,-0.5,9.95','P02,-1.0,9.95','P03,-2.0,9.95','P04,-4.0,9.95','P05,-8.0,9.95']
    
    file_out =  r'C:\Users\thomsonsj\OneDrive - AECOM\Documents\soil_results.csv'
    
    try:
        plx = GetPlaxisResults(host="ukcrdw1rc04g2",
                        port=10000,
                        password='39XW$k32f~h%PTD')
        if plx:
            plx.add_points_list (lst_pnts)
            plx.getSoilResultsByPointsSteps(fileOut=file_out,
                                    sphaseOrder='Phase_3,Phase_4')
    
    except Exception as e:
        print (str(e))
if __name__ == "__main__":
    main()