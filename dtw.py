import matplotlib.pyplot as plt
import numpy as np
from FileOperations import *


def distanceCostPlot(distances):
    im = plt.imshow(distances, interpolation=None, cmap='Reds')
    plt.gca().invert_yaxis()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.colorbar()


def calculateAccumulatedCost(signal1, signal2):
    accumulated_cost = np.zeros((len(signal2), len(signal1)))
    distances = calculateDistancesBetweenSignals(signal1, signal2)
    accumulated_cost[0, 0] = distances[0, 0]
    for i in range(1, len(signal1)):
        accumulated_cost[0, i] = distances[0, i] + accumulated_cost[0, i - 1]
    for i in range(1, len(signal2)):
        accumulated_cost[i, 0] = distances[i, 0] + accumulated_cost[i - 1, 0]
    for i in range(1, len(signal2)):
        for j in range(1, len(signal1)):
            accumulated_cost[i, j] = min(accumulated_cost[i - 1, j - 1], accumulated_cost[i - 1, j],
                                         accumulated_cost[i, j - 1]) + distances[i, j]
    return accumulated_cost


def calculateDistancesBetweenSignals(signal1, signal2):
    distances = np.zeros((len(signal2), len(signal1)))
    for i in range(len(signal2)):
        for j in range(len(signal1)):
            distances[i, j] = (signal1[j][1] - signal2[i][1]) ** 2
    return distances


def findWarpPath(signal1, signal2, accumulated_cost):
    path = [[len(signal1) - 1, len(signal2) - 1]]
    i = len(signal2) - 1
    j = len(signal1) - 1
    while i > 0 and j > 0:
        if i == 0:
            j = j - 1
        elif j == 0:
            i = i - 1
        else:
            if accumulated_cost[i - 1, j] == min(accumulated_cost[i - 1, j - 1], accumulated_cost[i - 1, j],
                                                 accumulated_cost[i, j - 1]):
                i = i - 1
            elif accumulated_cost[i, j - 1] == min(accumulated_cost[i - 1, j - 1], accumulated_cost[i - 1, j],
                                                   accumulated_cost[i, j - 1]):
                j = j - 1
            else:
                i = i - 1
                j = j - 1
        path.append([j, i])
    path.append([0, 0])
    return path


def plotWarpPath(path):
    path_x = [point[0] for point in path]
    path_y = [point[1] for point in path]
    plt.plot(path_x, path_y, 'k')


def show():
    plt.show()


def plotSignalsWithMinDistances(signal1, signal2, path, step):
    plt.plot(*zip(*signal1), label='signal 1')
    plt.plot(*zip(*signal2), label='signal 2')

    for idx_x, idx_y in path[0:len(path):step]:
        x1 = signal1[idx_x][0]
        y1 = signal1[idx_x][1]
        x2 = signal2[idx_y][0]
        y2 = signal2[idx_y][1]

        plt.plot([x1, x2], [y1, y2], color='k', linestyle='--', linewidth=1)

    plt.legend()
    plt.show()
