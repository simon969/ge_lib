from ge_lib.plaxis.PlaxisResults import GetPlaxisResults

plx = GetPlaxisResults(host="UKCRD1nnn",
                       port=10000,
                       password='')

plx.getSoilResultsByPoint()