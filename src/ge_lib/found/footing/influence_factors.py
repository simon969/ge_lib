import math

# ' ==========================================================================================
# ' Calculation of settlement influnce factors I1 and I2
# ' Foundation Settlements
# ' Bowles p303
# ' ==========================================================================================
# ' Coded  | Simon Thomson
# ' ==========================================================================================
# ' Company | AECOM
# ' ==========================================================================================
# ' Date    | Huly 2018
# ' ==========================================================================================
# ' Version | 01.00.00
# ' ==========================================================================================

def calc_I1(data):
        '''
        input parameters 
        ----------------
        Length factor : data.M
        Breadth factor : data.N
        
        output parameters
        -----------------
        Influence factor I1 : data.I1
        '''
        
        m2 = math.pow(data.M,2.0)
        n2 = math.pow(data.N,2.0)

        p1 = (1 + (m2 + 1) ^ 0.5) * (m2 + n2) ^ 0.5
        p2 = data.M * (1 + (m2 + n2 + 1) ^ 0.5)

        p3 = (data.M + (m2 + 1) ^ 0.5) * (1 + n2) ^ 0.5
        p4 = data.M + (m2 + n2 + 1) ^ 0.5

        data.I1 = 1 / math.pi * (data.M * math.log(p1 / p2) + math.log(p3 / p4))

def calc_I2(data):
        '''
        input parameters 
        ----------------
        Length factor : data.M
        Breadth factor : data.N
        
        output parameters
        -----------------
        Influence factor I2 : data.I2
        '''
         
        m2 = math.pow(data.M,2.0)
        n2 = math.pow(data.N,2.0)

        p1 = data.M / (data.N * (m2 + n2 + 1) ^ 0.5)
        
        data.I2 = data.N / (2 * math.pi) * math.atn(p1)

        return data.I2
