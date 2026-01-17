import numpy as np

class FileLoader_ResponseSpectrumCSV:
    def __init__(self,filePath):
        self.FilePath = filePath

    def Load(self):
        with open(self.FilePath,'r') as fil:
            lin = fil.readline().strip('\n').split(',')
            col1 = [itm.strip(' ').strip('\t').strip(']') for itm in lin[0].strip(' ').strip('\t').strip(']').split('[')]
            col2 = [itm.strip(' ').strip('\t').strip(']') for itm in lin[1].strip(' ').strip('\t').strip(']').split('[')]
            dat = fil.read().split('\n')
            dat = [itm.split(',') for itm in dat]
            dat = [[float(itm2) for itm2 in itm] for itm in zip(*dat)]
        if col1[1].lower() in ['hz','rad/s']:
            frequencyValues = np.array(dat[0])
            frequencyUnits = col1[1]
            ordinates = np.array(dat[1])
            ordinateUnits = col2[1]
        elif col1[2].lower() in ['hz','rad/s']:
            frequencyValues = np.array(dat[1])
            frequencyUnits = col2[1]
            ordinates = np.array(dat[0])
            ordinateUnits = col1[1]
        else:
            raise Exception(f'seismicmotions.fileloaders.responsespectrumcsv.ResponseSpectrumCsvFile.LoadFromFile: Frequency column not found. Example of compliant format is "f [Hz],Sa [g]" rather than "{",".join(lin)}".')

        return 'Absolute',ordinates,None,ordinateUnits,frequencyUnits,frequencyValues