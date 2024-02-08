from ge_lib.plaxis.PlaxisResults import Plaxis2dResultsConnectV22

try:
    plx = Plaxis2dResultsConnectV22(host="UKCRD1PC345871",
                    port=10000,
                    password='D@r>Srh1/vft9#ky')
    if plx:
        plx.getAllStructuralResults(folderOut="c:\\Temp", 
                                    sphaseOrder='Phase_23,Phase_24,Phase_26')

except Exception as e:
    print (str(e))