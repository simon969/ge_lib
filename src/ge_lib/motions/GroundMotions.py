from .Motions import Motion,  ReadTargetSpectrum,_ResponseSpectrum
from .Motions import COMPONENT_ACC_X, COMPONENT_ACC_Y, COMPONENT_ACC_Z
from .Motions import MotionComponentAcceleration2

from .PEERNGARecords import PEERFormatFile, ACCELERATION_EXT
from sys import os

def ReadPEERNGAAccelerations(filepath:str) -> list[Motion]:
    motions = []
    path = os.path.dirname(filepath)
    
    mr = PEERFormatFile()

    with open(filepath,'r') as fil:
        for i in range(0,1):
            lin = fil.readline()
        while True:
            lin = fil.readline()
            if not lin:
                break
            lin = lin.strip(' \n').split('\t')
            (xName,yName,zName) = lin
            print('Reading motion...')
            m =  Motion() 
            mr.FileName(path + xName + ACCELERATION_EXT)
            m.ReadData(mr,COMPONENT_ACC_X)
            mr.FileName(path + yName + ACCELERATION_EXT)
            m.ReadData(mr,COMPONENT_ACC_Y)
            mr.FileName(path + zName + ACCELERATION_EXT)
            m.ReadData(mr,COMPONENT_ACC_Z)
            motions.append(m)
    return motions

def ScaleMotion (motion:Motion,  targSpecHor: _ResponseSpectrum, targSpecVer:_ResponseSpectrum)-> Motion:
        scaled = Motion(motion.ParentFolder, motion.XName,motion.YName,motion.ZName)
        cx = motion.Accelerations.X.AccelerationsResponseSpectrum.ScalingFactorToMatch2(targSpecHor)
        cy = motion.Accelerations.Y.AccelerationsResponseSpectrum.ScalingFactorToMatch2(targSpecHor)
        cz = motion.Accelerations.Z.AccelerationsResponseSpectrum.ScalingFactorToMatch2(targSpecVer)
        
        accXScaled = MotionComponentAcceleration2(motion.Accelerations.X.Title,motion.Accelerations.X.TimeStep,cx*motion.Accelerations.X.Values)
        accYScaled = MotionComponentAcceleration2(motion.Accelerations.Y.Title,motion.Accelerations.Y.TimeStep,cy*motion.Accelerations.Y.Values)
        accZScaled = MotionComponentAcceleration2(motion.Accelerations.Z.Title,motion.Accelerations.Z.TimeStep,cz*motion.Accelerations.Z.Values)
        return scaled

def OutputToToPEERFormatFile(pathFrom:str,pathTo) -> None:
        with open(pathFrom,'r') as fil:
            lin = fil.readline().strip('\t \n')
            newFileName = lin.split(': ')[1]
            lin = fil.readline()
            lin = fil.readline().strip('\t \n')
            lin = lin.split(': ')[1].split(' ')[0]
            timeStep = float(lin)
            lin = fil.readline()
            lin = fil.readline()
            accs = []
            while True:
                lin = fil.readline()
                if not lin:
                    break
                lin = lin.strip('\t \n').split('\t')
                accs.append(float(lin[-1]))
        accs = MotionComponentAcceleration2('No title',timeStep,np.array(accs))
        accs.WriteToPEERFormatFile(pathTo + '\\' + newFileName)    

def CreateMotionPEERFormatFile()->Motion

def ReadMotions(path:str) -> list[Motion]:
    motions = []
    with open(path + '\\fileNames.txt','r') as fil:
        for i in range(0,1):
            lin = fil.readline()
        while True:
            lin = fil.readline()
            if not lin:
                break
            lin = lin.strip(' \n').split('\t')
            [xName,yName,zName] = lin
            print('Reading motion...')
            motions.append(Motion(path,xName,yName,zName))
    return motions


def ScaleAll() -> None:
    targSpecHor = ReadTargetSpectrum(r'C:\Users\EmmanouilZ\OneDrive - AECOM\Home Drive\works\Project six\03. Target spectrum\target spectrum horizontal.txt')
    targSpecVer = ReadTargetSpectrum(r'C:\Users\EmmanouilZ\OneDrive - AECOM\Home Drive\works\Project six\03. Target spectrum\target spectrum vertical.txt')
    motions = ReadMotions(r'C:\Users\EmmanouilZ\OneDrive - AECOM\Home Drive\works\Project six\03. Target spectrum\PEERNGARecords_Unscaled')
    for motion in motions:
        cx = motion.Accelerations.X.AccelerationsResponseSpectrum.ScalingFactorToMatch2(targSpecHor)
        cy = motion.Accelerations.Y.AccelerationsResponseSpectrum.ScalingFactorToMatch2(targSpecHor)
        cz = motion.Accelerations.Z.AccelerationsResponseSpectrum.ScalingFactorToMatch2(targSpecVer)
        accXScaled = MotionComponentAcceleration2(motion.Accelerations.X.Title,motion.Accelerations.X.TimeStep,cx*motion.Accelerations.X.Values)
        accYScaled = MotionComponentAcceleration2(motion.Accelerations.Y.Title,motion.Accelerations.Y.TimeStep,cy*motion.Accelerations.Y.Values)
        accZScaled = MotionComponentAcceleration2(motion.Accelerations.Z.Title,motion.Accelerations.Z.TimeStep,cz*motion.Accelerations.Z.Values)
        accXScaled.WriteToPEERFormatFile(r'C:\Users\EmmanouilZ\OneDrive - AECOM\Home Drive\works\Project six\03. Target spectrum\PEERNGARecords_scaled2' + '\\' + motion.Accelerations.X.FileName)
        accYScaled.WriteToPEERFormatFile(r'C:\Users\EmmanouilZ\OneDrive - AECOM\Home Drive\works\Project six\03. Target spectrum\PEERNGARecords_scaled2' + '\\' + motion.Accelerations.Y.FileName)
        accZScaled.WriteToPEERFormatFile(r'C:\Users\EmmanouilZ\OneDrive - AECOM\Home Drive\works\Project six\03. Target spectrum\PEERNGARecords_scaled2' + '\\' + motion.Accelerations.Z.FileName)
def SeismoMatchOutputToToPEERFormatFile(s):
    pass
def SeismoMatchOutputToToPEERFormatFileAll() -> None:
    pathsFrom = [r'C:\Users\EmmanouilZ\OneDrive - AECOM\Home Drive\works\Project six\03. Target spectrum\PEERNGARecords_modified\1',
                 r'C:\Users\EmmanouilZ\OneDrive - AECOM\Home Drive\works\Project six\03. Target spectrum\PEERNGARecords_modified\2']
    for pathFrom in pathsFrom:
        for fileName in os.listdir(pathFrom):
            SeismoMatchOutputToToPEERFormatFile(pathFrom + '\\' + fileName,r'C:\Users\EmmanouilZ\OneDrive - AECOM\Home Drive\works\Project six\03. Target spectrum\PEERNGARecords_modified')

