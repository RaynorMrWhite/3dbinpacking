import sortieralgorithmen
import guetefunktionen
#dataset = [[39, 85, 72], [11, 84, 96], [36, 10, 34], [12, 76, 71], [64, 73, 56], [26, 77, 97], [30, 23, 17], [46, 27, 47], [47, 69, 67], [29, 71, 98], [88, 69, 64], [47, 95, 99], [20, 95, 93], [23, 8, 32], [67, 73, 55], [69, 46, 95], [47, 80, 85]]


#adds placementpoints along the axis to CornerPointList
def updateCornerPoints(itemtoadd, CornerPointList):
    CornerPointList.append((itemtoadd[0] + itemtoadd[3], itemtoadd[1], itemtoadd[2]))
    CornerPointList.append((itemtoadd[0], itemtoadd[1] + itemtoadd[4], itemtoadd[2]))
    CornerPointList.append((itemtoadd[0], itemtoadd[1], itemtoadd[2] + itemtoadd[5]))
    sortieralgorithmen.sortZYX(CornerPointList)


#returns list of items within bin, where items are packed on the first possible point
def CornerPointFirstFit(items, bin_size, CornerPointList, feasibleSolution):
    for n, item in enumerate(items):
        # on first iteration
        if n == 0 and feasibleSolution == [[]]:
            feasibleSolution[0].append([0, 0, 0, item[0], item[1], item[2]])
            CornerPointList.append([(item[0], 0, 0), (0, item[1], 0), (0, 0, item[2])])
        else:
            # searches for first fitting Point
            newCornerPoint = guetefunktionen.determinePlacementPoint(feasibleSolution, item, bin_size, CornerPointList)
            # places point
            if newCornerPoint is not None:
                itemToAdd = [newCornerPoint[0][0], newCornerPoint[0][1], newCornerPoint[0][2], item[0], item[1], item[2]]
                feasibleSolution[newCornerPoint[1]].append(itemToAdd)
                updateCornerPoints(itemToAdd, CornerPointList[newCornerPoint[1]])
                CornerPointList[newCornerPoint[1]].remove(newCornerPoint[0])
                CornerPointList[newCornerPoint[1]] = sortieralgorithmen.sortZYX(CornerPointList[newCornerPoint[1]])
            # if there is no point in a bin to Place
            if newCornerPoint is None:
                feasibleSolution.append([[0, 0, 0, item[0], item[1], item[2]]])
                CornerPointList.append([(item[0], 0, 0), (0, item[0], 0), (0, 0, item[0])])
    return feasibleSolution, CornerPointList


# returns list of items within bin, where items are packed in the bin with the least volume after playment
def CornerPointBestFitbyVolume(items, bin_size, CornerPointList, feasibleSolution):
    for n, i in enumerate(items):
        packed = 0
        # on first iteration
        if n == 0 and feasibleSolution == [[]]:
            feasibleSolution[0].append([0, 0, 0, i[0], i[1], i[2]])
            CornerPointList.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
        else:
            # searches for optimal Point
            nep = guetefunktionen.determinePlacementPointLeastFreeVolume(feasibleSolution, i, bin_size, CornerPointList)
            # places item in bin
            if nep is not None:
                nitem = [nep[0][0], nep[0][1], nep[0][2], i[0], i[1], i[2]]
                feasibleSolution[nep[1]].append(nitem)
                updateCornerPoints(nitem, CornerPointList[nep[1]])
                CornerPointList[nep[1]].remove(nep[0])
            # if there is no point in a bin to Place
            if nep is None:
                feasibleSolution.append([[0, 0, 0, i[0], i[1], i[2]]])
                CornerPointList.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
    return feasibleSolution, CornerPointList


# returns list of items within bins, packed on the point where the most residual space is taken
def CornerPointBestFitbyResidualSpace(items, bin_size, CornerPointList, feasibleSolution):
    for n, i in enumerate(items):
        # on first iteration
        if n == 0 and feasibleSolution == [[]]:
            feasibleSolution[0].append([0, 0, 0, i[0], i[1], i[2]])
            CornerPointList.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
        else:
            # searches for optimal Point
            indexofbin, nep = guetefunktionen.determineMaxResPlacementPoint(i, CornerPointList, bin_size, feasibleSolution)
            # places item in bin
            if nep is not None:
                nitem = [nep[0], nep[1], nep[2], i[0], i[1], i[2]]
                feasibleSolution[indexofbin].append(nitem)
                updateCornerPoints(nitem, CornerPointList[indexofbin])
                CornerPointList[indexofbin].remove(nep)
            # if there is no point in a bin to Place
            if nep is None:
                feasibleSolution.append([[0, 0, 0, i[0], i[1], i[2]]])
                CornerPointList.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
    return feasibleSolution, CornerPointList

