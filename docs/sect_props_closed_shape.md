# Section Properties of Closed Shape

Determine the section properties of closed shapes

Supply coordinate pairs of a planar closed polygon and the section properties are calculated

Example Rectangular Section
----
We provide the coordinates of a 1.2m deep by 0.6m wide rectangular section and use closed form solutions to compare the results



```python
from ge_lib.general.section_props.SectionProperties import SectionProperties 

    data = {"coords":[
                [0,0],
                [0,1.2],
                [0.6,1.2],
                [0.6,0],
                [0,0]
                ],
                "units":"m"
                }
    sp =  SectionProperties()
    values, symbols, description, units = sp.calc_props(data)
    result = { "symbols":symbols,
               "description":description,
               "units": units,
               "values":values} 
    print (result)
```
result:

```json
{
    "symbols": [
        "Area",
        "AX",
        "AY",
        "IX",
        "IY",
        "IXY",
        "Xc",
        "Yc",
        "IXC",
        "IYC",
        "IXYC",
        "IU",
        "IV",
        "Theta"
    ],
    "description": [
        "Section area",
        "First moment of area about the X axis",
        "First moment of area about the Y axis",
        "Second Moment of Area about the X axis",
        "Second Moment of Area about the Y axis",
        "Product of Inertia about origin",
        "Centroid X coordinate",
        "Centroid Y coordinate",
        "2nd Moment of Area about axis through the centroid parallel to X",
        "2nd Moment of Area about axis through the centroid parallel to Y",
        "Product of Inertia about centroid",
        "2nd moment of area about principal axis 1 through centroid",
        "2nd moment of area about principal axis 2 through centroid",
        "Angle of principal axes to X,Y axes"
    ],
    "units": [
        "m2",
        "m3",
        "m3",
        "m4",
        "m4",
        "m4",
        "m",
        "m",
        "m4",
        "m4",
        "m4",
        "m4",
        "m4",
        "degrees"
    ],
    "values": [
        0.72,
        0.432,
        0.216,
        0.34559999999999996,
        0.08639999999999999,
        0.12960000000000002,
        0.3,
        0.6,
        0.08639999999999998,
        0.021599999999999994,
        2.7755575615628914e-17,
        0.08639999999999998,
        0.021599999999999994,
        0
    ]
}
```
Comparison with section properties calculated from formulae for rectangular section 
---
|Property                  |Units |From formulae        |From function |Error (%)|
|--------------------------|------|---------------------|--------------|---------|
|Area (AX)	               |bd    |1.2*0.6 = 0.72       |0.72	       |0        |
|Second Moment of Area (IX)|bd<sup>3</sup>/12|0.6*1.2^3/12 = 0.864 |0.8639999     |0        |
|Second Moment of Area (IY)|db<sup>3</sup>/12|1.2*0.6^3/12 = 0.0216|0.2159999	   |0        |


Example UC Section
-----
We provide the coordinates of a structural a structural steel section in mm (356 x 406 x 634 x 633.9kg/m UC) and use the published geometry of to compare the results


```python
from ge_lib.general.section_props.SectionProperties import SectionProperties 

 # 356 x 406 x 634 x 633.9kg/m UC
    data = {"name":"356x406x634x633.9kg/m",
            "coords":[
                        [0,0],
                        [0,77],
                        [188.2,77],
                        [188.2,397.6],
                        [0,397.6],
                        [0,474.6],
                        [424,474.6],
                        [424,397.6],
                        [235.8,397.6],
                        [235.8,77],
                        [424,77],
                        [424,0],
                        [0,0]],
            "units":"mm"}

    
    sp =  SectionProperties()

    values, symbols, description, units = sp.calc_props(data)
    result = {"symbols":symbols,
                "description":description,
                "units": units,
                "values":values} 
    print (result)
```
result:

```json
{
 "symbols": [
        "Area",
        "AX",
        "AY",
        "IX",
        "IY",
        "IXY",
        "Xc",
        "Yc",
        "IXC",
        "IYC",
        "IXYC",
        "IU",
        "IV",
        "Theta"
    ],
    "description": [
        "Section area",
        "First moment of area about the X axis",
        "First moment of area about the Y axis",
        "Second Moment of Area about the X axis",
        "Second Moment of Area about the Y axis",
        "Product of Inertia about origin",
        "Centroid X coordinate",
        "Centroid Y coordinate",
        "2nd Moment of Area about axis through the centroid parallel to X",
        "2nd Moment of Area about axis through the centroid parallel to Y",
        "Product of Inertia about centroid",
        "2nd moment of area about principal axis 1 through centroid",
        "2nd moment of area about principal axis 2 through centroid",
        "Angle of principal axes to X,Y axes"
    ],
    "units": [
        "mm2",
        "mm3",
        "mm3",
        "mm4",
        "mm4",
        "mm4",
        "mm",
        "mm",
        "mm4",
        "mm4",
        "mm4",
        "mm4",
        "mm4",
        "degrees"
    ],
    "values": [
        80556.56,
        19116071.688000005,
        17077990.720000003,
        7279809664.205869,
        4601636571.1754675,
        4052607197.8560004,
        212.00000000000003,
        237.30000000000007,
        2743565852.643466,
        981102538.5354662,
        -0.000001430511474609375,
        2743565852.643466,
        981102538.5354662,
        -4.6504383599970096e-14
    ]
}
   
```
Comparison with published section properties
---
|Property                  |Units|	Published|	Calculated	|Error (%)|
|--------------------------|-----|-----------|--------------|---------|
|Area (AX)	               |mm2	 |80800	     |80557	        |-0.301   |
|Second Moment of Area (IX)|mm4	 |2748000000 |2743565853	|-0.161   |
|Second Moment of Area (IY)|mm4	 |981300000	 |981102539	    |-0.020   |

