import numpy as np
from fractions import Fraction as fc

class FileLoader_PEER:
    def __init__(self,filePath):
        self.FilePath = filePath

    def Load(self):
        with open(self.FilePath,'r') as fil:
            fil.readline()
            fil.readline()
            lin = fil.readline()
            units = lin.lower().split(' in units of ')[1].strip()
            lin = fil.readline()
            lin = lin.split(',')
            pointsNo = int(lin[0].split('=')[1].strip())
            lin = lin[1].split('=')[1].strip()
            timeUnits = ''.join([itm for itm in lin if not itm.isdigit() and itm != '.' and itm != ' '])
            if timeUnits.lower() != 'sec':
                fileName = self.FilePath.split("\\")[-1]
                raise Exception(f'seismicmotions.fileloaders.FileLoader_PEER: Time step in file {fileName} is not in seconds.')
            timeStep = fc(lin[0:-len(timeUnits)].strip())
            lin = fil.read()
            lin = lin.replace('\n',' ').split(' ')
            lin = [float(itm) for itm in lin if itm != '']
            lin = np.array(lin)
            if lin.size != pointsNo:
                fileName = self.FilePath.split("\\")[-1]
                raise Exception(f'seismicmotions.fileloaders.FileLoader_PEER: Number of points in {fileName} is different from what is written at the file''s headings.')
            fileExtension = self.FilePath.split('.')[-1].strip().lower()
        if fileExtension == 'at2':
            return timeStep,pointsNo,lin,units,None,'?',None,'?'
        elif fileExtension == 'vt2':
            return timeStep,pointsNo,None,'?',lin,units,None,'?'
        elif fileExtension == 'dt2':
            return timeStep,pointsNo,None,'?',None,'?',lin,units