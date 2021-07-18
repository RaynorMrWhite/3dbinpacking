import statistics
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook


def calculateMeanOfLists(list):
    res = []

    for j in range(32):
        meanbin = []
        sumofTime = []
        meanoftime = []
        for i in range(10):
            meanbin.append(list[i][j][0])
            sumofTime.append(list[i][j][1])
            meanoftime.append(list[i][j][2])
        res.append([statistics.mean(meanbin), statistics.mean(sumofTime), statistics.mean(meanoftime)])
    return res

