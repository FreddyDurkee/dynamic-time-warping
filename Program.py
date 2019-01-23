from fastdtw import fastdtw
from FileOperations import *
import matplotlib.pyplot as plt
import dtw
import numpy as np


def moveTimeAxis(signal, distance):
    signal[:, 0] = signal[:, 0] + distance

    return signal


def noiseSignal(signal):
    signal[:, 1] = np.array([signal[i][1] * np.random.randint(1, 100) / 100 for i in range(len(signal))])

    return signal


def speedUpSignal(xTimes, signal):
    signal = np.array(signal)[::xTimes]
    # signal[:, 0] = signal[:, 0]

    return signal


def generateSignalFromRecords(signalX, signalY):
    return np.vstack((np.array(signalX), np.array((signalY)))).T


def displayResults(signal1, signal2, path, step):
    plt.plot(*zip(*signal1), label='arrythmia')
    plt.plot(*zip(*signal2), label='arrythmiaTreatment')

    for idx_x, idx_y in path[0:len(path):step]:
        x1 = signal1[idx_x][0]
        y1 = signal1[idx_x][1]
        x2 = signal2[idx_y][0]
        y2 = signal2[idx_y][1]

        plt.plot([x1, x2], [y1, y2], color='k', linestyle='--', linewidth=1)

    plt.legend()
    plt.show()


def generateTrialSignals():
    x1 = np.arange(0, 10, 0.1)
    y1 = np.sin(np.arange(0, 10, 0.1)) * 10
    x2 = np.arange(0, 10, 0.1)
    y2 = np.array([y1[i] * np.random.randint(1, 100) / 100 for i in range(len(x2))])

    signal1 = np.vstack((x1, y1)).T
    signal2 = np.vstack((x2, y2)).T

    return signal1, signal2


def calculateDtwDistances(signal1, signal2):
    distances = np.zeros((len(signal1), len(signal2)))
    for i in range(len(signal1)):
        for j in range(len(signal2)):
            distances[i, j] = (signal2[j][1] - signal1[i][1]) ** 2
    return distances


def main():
    # Patient data: https://physionet.org/physiobank/database/ptbdb/patient294/
    timeSleep,  sleppSignal = readDatFile("sleepECG.csv")
    # timeArythmiaSignal, arythmiaSignal = readDatFile("eck_arrythmia.csv")
    #
    sleepSignalZip = generateSignalFromRecords(timeSleep, sleppSignal)
    #
    # refSignal1 = refSignal[280:400]
    # refSignal2 = refSignal[680:800] + 0.5
    #

    sleepSignalBegin = sleepSignalZip[400:700]
    sleepSignalEnd = sleepSignalZip[14000:14300]
    acc = dtw.calculateAccumulatedCost(sleepSignalBegin, sleepSignalEnd)
    path = dtw.findWarpPath(sleepSignalBegin, sleepSignalEnd, acc)

    dtw.plotSignalsWithMinDistances(sleepSignalBegin, sleepSignalEnd, path, 20)
    dtw.distanceCostPlot(acc)
    dtw.plotWarpPath(path)

    dtw.show()

    # plt.plot(sleppSignal)
    # plt.show()


if __name__ == '__main__':
    main()
