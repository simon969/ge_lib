import numpy as np
from fractions import Fraction as fc

class FileLoader_DEEPSOIL:
    def __init__(self,filePath):
        self.FilePath = filePath

    def Load(self):
        a = []
        with open(self.FilePath,'r') as fil:
            ln = fil.readline().strip('\n').replace(' ','\t').split('\t')
            ts = fc(ln[1])
            while True:
                ln = fil.readline()
                if ln == '':
                    break
                ln = ln.strip('\n').replace(' ','\t').split('\t')
                a.append(float(ln[1]))
        if a[0] != fc('0'):
            a = [0] + a
        a = np.array(a)
        return ts,a.size,a,'?',None,'?',None,'?'