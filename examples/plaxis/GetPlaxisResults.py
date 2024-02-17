def main():

    test_getSoilResults()


def test_getAllStructuralResults():
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

if __name__ == "__main__":
    main()