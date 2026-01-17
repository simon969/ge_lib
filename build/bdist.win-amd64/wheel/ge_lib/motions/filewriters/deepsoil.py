class FileWriter_DEEPSOIL:
    def __init__(self,filePath):
        self.FilePath = filePath

    def Write(self,motion):
        timeStep = motion.TimeStep
        pointsNo = motion.PointsNo
        aVals = motion.MotionComponents.a.Values
        with open(self.FilePath,'w') as fil:
            fil.write(pointsNo.__str__() + ' ' + timeStep.__str__() + '\n')
            dataToWrite = '\n'.join([' '.join([itmij.__str__() for itmij in itmi]) for itmi in zip([timeStep*i for i in range(0,pointsNo)],aVals)])
            fil.write(dataToWrite)

class FileWriter_DEEPSOIL_float:
    def __init__(self,filePath):
        self.FilePath = filePath

    def Write(self,motion):
        timeStep = motion.TimeStep
        pointsNo = motion.PointsNo
        aVals = motion.MotionComponents.a.Values
        with open(self.FilePath,'w') as fil:
            fil.write(pointsNo.__str__() + ' ' + timeStep.__float__().__str__() + '\n')
            dataToWrite = '\n'.join([' '.join([itmij.__float__().__str__() for itmij in itmi]) for itmi in zip([timeStep*i for i in range(0,pointsNo)],aVals)])
            fil.write(dataToWrite)