import numpy as np
# ' ==========================================================================================
# ' Calculation of depth factors
# '
# ' ==========================================================================================
# ' Coded  | Simon Thomson
# ' ==========================================================================================
# ' Company | AECOM
# ' ==========================================================================================
# ' Date    | Huly 2018
# ' ==========================================================================================
# ' Version | 01.00.00
# ' ==========================================================================================

# Length/Breadth = 5, Poisson Ration = 0.5
depth_factors_5_05 = [0.930,0.910,0.895,0.875,0.860,0.850,0.750,0.690,0.650,0.625,0.558]

# Length/Breadth = 5, Poisson Ratio = 0.3
depth_factors_5_03 = [0.870,0.850,0.830,0.810,0.795,0.780,0.675,0.620,0.585,0.565,0.510]

# Length/Breadth = 1, Poisson Ratio = 0.5
depth_factors_1_05 = [0.860,0.822,0.790,0.765,0.745,0.725,0.625,0.590,0.570,0.555,0.525]

# Length/Breadth = 1, Poisson Ratio = 0.3
depth_factors_1_03 = [0.775,0.740,0.715,0.690,0.670,0.650,0.565,0.530,0.515,0.500,0.500]

# Depth/Breadth ratios 0.5 to 10
db_ratios = [0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,10]

def calc_depth_factor(data):
    '''
    input parameters 
    ----------------
    Length : data.Length
    Breadth : data.Breadth
    Depth : data.Depth
    PoissonRatio : data.Poisson

    output parameters
    -----------------
    Length/Breadth ratio : data.LBratio
    Depth/Breadth ratio : data.DBratio
    DepthFactor : data.DepthFactor

    '''
    data.LBratio = data.Length / data.Breadth
    data.DBratio = data.Depth / data.Breadth

    valLB1P3 = np.interp(data.DBratio, depth_factors_1_03)
    valLB5P3 = np.interp(data.DBratio, depth_factors_5_03)
    valLB1P5 = np.interp(data.DBratio, depth_factors_1_05)
    valLB5P5 = np.interp(data.DBratio, depth_factors_5_05)
    
    if (data.LBratio > 1):
        LBFactor = (data.LBratio - 1) / (5 - 1)
    else:
        LBFactor = 0
    
    if (data.Poisson > 0.3):
        PoissonFactor = (data.Poisson - 0.3) / (0.5 - 0.3)
    else:
        PoissonFactor = 0 

    valP3 = (valLB5P3 - valLB1P3) * LBFactor + valLB1P3
    valP5 = (valLB5P5 - valLB1P5) * LBFactor + valLB1P5
    
    data.DepthFactor = (valP5 - valP3) * PoissonFactor + valP3
    
    return data.DepthFactor