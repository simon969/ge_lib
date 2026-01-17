import numpy as np

class FileWriter_ResponseSpectrumCSV:
    def __init__(self,filePath):
        self.FilePath = filePath

    def Write(self,responseSpectrum):
        with open(self.FilePath,'w') as fil:
            fil.write(f'f [{responseSpectrum.Frequencies.Units}],Sa [{responseSpectrum.Parent.MotionComponents.a.Units}]\n')
            data = '\n'.join([f'{f},{sa}' for f,sa in zip(responseSpectrum.Frequencies.Values,responseSpectrum.Values.a.Ordinates)])
            fil.write(data)