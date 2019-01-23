import numpy as np
import os

def readDatFile(fileName):

    fileName = os.path.join("Input", fileName)
    data = np.genfromtxt(fileName,
                         dtype=str,
                         skip_header=2,
                         delimiter=',',
                         usecols=[0, 1])

    myData = np.array([
        (float(twoData[0][1:-1].split(":")[0]) * 60 +
         float(twoData[0][1:-1].split(":")[1]),
        float(twoData[1])) for twoData in data])

    return myData[:, 0], myData[:, 1]