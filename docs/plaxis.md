## Plaxis Results
============================

A results class for each of the plaxis versions will connect to the host output server and will request selected results and phases from the output model

| plx.getAllStructuralResults(param list)
| plx.getInterfaceResults(param list)
| plx.getPlateResults(param list)
| plx.getEmbeddedBeamResults(param list)

where param list may contain

**folderOut:** 'c:\\temp', Any | None = None

| The folder that the results should be saved to

**fileOut:** 'myfile.csv', Any | None = None

| The file name that will be used to save the data. The file name extention will tell the function which format is required.
| "*.mdb" Access database file* 
| "*.csv" Comma Separated Value text file*

**tableOut:** Any | None = None

| The table name that will be used if the data is saved in a database storage system

**sphaseOrder:** Any | None = None

| List of phases to be included in returned data for example 'Phase_1,Phase_24,Phase_30' if left blank it will be taken as all phases between the sPhaseStart and sPhaseEnd parameters

**sphaseStart:** Any | None = None,

| First phase to be included in returned data for example 'Phase_1' if left blank it will be taken as the first phase in the output

**sphaseEnd:** Any | None = None

| Last phase to be included in returned data for example 'Phase_24' if left blank it will be the last phase in the output


Implementation
--------------
A connection to the host server can be established and the appropriate version of the plaxis result class is returned, this is achieved using the GetPlaxisResults function as detailed below

```python
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
```

Juypter Notebook
----------------
We have created an example Juypter Notebook which connects to the Plaxis 2D Output program and extracts structural results dfor selected phases
[See here](/examples/plaxis/Plaxis2D_StructuralResults.ipynb)


::: ge_lib.plaxis.PlaxisResults
    handler: python
    options:
      inherited_members: true
      members: true


Version Changes
----------------------

Plaxis3dResults2024
No change

Plaxis2dResults2024
No changes required

Plaxis2dResults2023
MaterialId changed to MaterialIndex  

Plaxis3dResults2023
MaterialId changed to MaterialIndex  

Plaxis2dResultsConnectV22
2024/10/06 added 
    getInterfaceDynamicSingleResultsByPointsByStep(steps,PhaseName,fileOut,tableOut=None,mode),
    getInterfaceDynamicResultsByPointsByStep(steps,PhaseName,fileOut,tableOut=None,mode)
    getSoilDynamicSingleResultsByPointsByStep(steps,PhaseName,fileOut,tableOut=None,mode),
    getSoilDynamicResultsByPointsByStep(steps,PhaseName,fileOut,tableOut=None,mode)

Plaxis3dResultsConnect
2024/10/06 added 
    getInterfaceDynamicSingleResultsByPointsByStep (steps,PhaseName,fileOut,tableOut=None,mode)
    getInterfaceDynamicResultsByPointsByStep (steps,PhaseName,fileOut,tableOut=None,mode)
    getSoilDynamicSingleResultsByPointsByStep (steps,PhaseName,fileOut,tableOut=None,mode)
    getSoilDynamicResultsByPointsByStep (steps,PhaseName,fileOut,tableOut=None,mode)