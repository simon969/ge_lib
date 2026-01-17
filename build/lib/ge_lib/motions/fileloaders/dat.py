import numpy as np
from fractions import Fraction as fc

class FileLoader_DAT:
    def __init__(self,filePath):
        self.FilePath = filePath

    def Load(self):
        t = []
        a = []
        v = []
        d = []
        with open(self.FilePath,'r') as fil:
            units = fil.readline().rstrip('\n').split(' ')
            units = [itm for itm in units if itm != '']
            units = [itm.split('(')[1] for itm in units if '(' in itm]
            units = [itm.split(')')[0] for itm in units if ')' in itm]
            ln = fil.readline()
            ln = fil.readline()
            while True:
                ln = fil.readline().rstrip('\n')
                if ln == '':
                    break
                ln = ln.split(' ')
                ln = [itm for itm in ln if itm != '']
                t.append(fc(ln[0]))
                a.append(float(ln[1]))
                v.append(float(ln[2]))
                d.append(float(ln[3]))
        t = np.array(t)
        a = np.array(a)
        v = np.array(v)
        d = np.array(d)
        tu = np.unique(np.round(t[1:]-t[0:-1],10))
        if tu.size != 1:
            fileName = self.FilePath.split("\\")[-1]
            raise Exception(f'seismicmotions.fileloaders.FileLoader_DAT: Time values in file {fileName} do not have unique time step.')
        return tu[0],a.size,a,units[1],v,units[2],d,units[3]