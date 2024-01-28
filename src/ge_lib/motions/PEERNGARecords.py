import os
import numpy as np
from .Motions import Motion

DISPLACEMENT_EXT = 'DT2'
VELOCITY_EXT = 'VT2'
ACCELERATION_EXT = 'AT2'

class PEERFormatFile():
    
    def FileName (self,filePath:str ):
        t = filePath.rfind('\\')
        self.ParentFolder = filePath[0:t]
        self.FileName = filePath[t+1:]
    
    def ReadFromFile(self) -> tuple[str,int,float,np.array]:
        fil = open(self.ParentFolder + '\\' + self.FileName,'r')
        lin = fil.readline()
        lin = fil.readline()
        title = lin.strip(' \n')
        lin = fil.readline()
        lin = fil.readline().split(',')
        npts = int(lin[0].strip(' \n')[len('NPTS='):])
        dt = float(lin[1].strip(' \n')[len('DT='):-len('SEC')])
        values:list[float] = []
        while True:
            lin = fil.readline().strip(' \n')
            if not lin:
                break
            lin = lin.split(' ')
            for itm in lin:
                if itm!='':
                    values.append(float(itm))
        fil.close()
        values = np.array(values)
        if np.size(values) != npts:
            raise ValueError('Motion.ReadFromFile: Number of points written in file does not match points count')
        return (title,npts,dt,values)
    
    def FormatTimestep(ts:float) -> str:
            res = round(ts,4).__str__()
            if res.find('.') == -1:
                res = res.lstrip('0').rjust(8)
            else:
                res = res.split('.')
                if int(res[0]) == 0:
                    res = '.' + res[1].rstrip('0') + '0'*(4-len(res[1]))
                    res = res.rjust(8)
                else:
                    res = res[0].lstrip('0') + '.' + res[1].rstrip('0') + '0'*(4-len(res[1]))
                    res = res.rjust(8)
            return res
    def FormatValue(val:float) -> str:
            res = ' ' if val >= 0 else '-'
            valT = abs(val)
            if valT == 0:
                res += '.' + '0'*7 + 'E+00'
            else:
                if valT > 1:
                    i = 0
                    while valT > 1:
                        i += 1
                        valT /= 10
                    i = i
                else:
                    i = 0
                    while valT < 1:
                        i += 1
                        valT *= 10
                    i = -(i-1)
                valT = abs(val)*(10**(-i))
                valT = round(valT,7).__str__().lstrip('0.').rstrip('0')
                valT += '0'*(7-len(valT))
                res += '.' + valT + 'E' + ('+' if i >=0 else '-') + int(abs(i)).__str__().zfill(2)
            return res
    
    def WriteToPEERFormatFile (self, m:Motion, filePath:str) -> None:
        self.FileName(filePath)
        with open(filePath,'w') as fil:
            fil.write('PEER NGA STRONG MOTION DATABASE RECORD\n')
            fil.write(self.Title + '\n')
            fil.write('ACCELERATION TIME SERIES IN UNITS OF G\n')
            fil.write(f'NPTS={m.PointsNo.__str__().rjust(7)}, DT={m.FormatTimestep(m.TimeStep)} SEC\n')
            for i in range(0,m.PointsNo//5):
                for j in range(0,5):
                    fil.write(f'  {m.FormatValue(m.Values[5*i+j])}')
                fil.write('\n')
            for i in range(0,m.PointsNo%5):
                fil.write(f'  {m.FormatValue(m.Values[m.PointsNo//5*5-1+i])}')
            if m.PointsNo%5 > 0:
                fil.write(' '*(5-m.PointsNo%5)*15)
    
    