import sortieralgorithmen
import guetefunktionen

#inspired by https://stackoverflow.com/questions/43170526/extreme-point-based-packing-algorithm-3d
# defines if the Y coordinate of item onto the X-Axis where it intersects with X of the packedItem
def CanTakeProjectionYx(item, packedItem):
    return item[0] >= packedItem[0] + packedItem[3] and item[1] + item[4] < packedItem[1] + packedItem[4] and item[2] < packedItem[2] + packedItem[5]


# defines if the Y coordinate of item onto the Z-Axis where it intersects with Z of the packedItem
def CanTakeProjectionYz(item, packedItem):
    return item[2] >= packedItem[2] + packedItem[5] and item[1] + item[4] < item[1] + packedItem[4] and item[0] < packedItem[0] + packedItem[3]


# defines if the X coordinate of item onto the Y-Axis where it intersects with Y of the packedItem
def CanTakeProjectionXy(item, packedItem):
    return item[1] >= packedItem[1] + packedItem[4] and item[0] + item[3] < packedItem[0] + packedItem[3] and item[2] < packedItem[2] + packedItem[5]


# defines if the X coordinate of item onto the Z-Axis where it intersects with Z of the packedItem
def CanTakeProjectionXz(item, packedItem):
    return item[2] >= packedItem[2] + packedItem[5] and item[0] + item[3] < packedItem[0] + packedItem[3] and item[1] < packedItem[1] + packedItem[4]


# defines if the Z coordinate of item onto the X-Axis where it intersects with X of the packedItem
def CanTakeProjectionZx(item, packedItem):
    return item[0] >= packedItem[0] + packedItem[3] and item[2] + item[5] < packedItem[2] + packedItem[5] and item[1] < packedItem[1] + packedItem[4]


# defines if the Z coordinate of item onto the Y-Axis where it intersects with Y of the packedItem
def CanTakeProjectionZy(item, packedItem):
    return item[1] >= packedItem[1] + packedItem[4] and item[2] + item[5] < packedItem[2] + packedItem[5] and item[0] < packedItem[0] + packedItem[3]


# bin: contains all items of the considered bin
# DEPL: List of Extremepoints for item which is considered to be added to the bin
# nEP: Extremepoint for the new Item
# returns a List of new Extremepoints
#based on Crainic(2008) Extreme Point-Based Heuristics for Three-Dimensional Bin Packing
def update3DEPL(itemtoadd, DEPL, bin, nEp):
    maxBound = [-1, -1, -1, -1, -1, -1]
    neweps = []
    for i in bin:
        if CanTakeProjectionYx(itemtoadd, i) and i[0] + i[3] > maxBound[2]:
            neweps.append((i[0] + i[3], itemtoadd[1] + itemtoadd[4], itemtoadd[2]))
            maxBound[2] = i[0] + i[3]

        if CanTakeProjectionYz(itemtoadd, i) and i[2] + i[5] > maxBound[3]:
            neweps.append((itemtoadd[0], itemtoadd[1] + itemtoadd[4], i[2] + i[5]))
            maxBound[3] = i[2] + i[5]

        if CanTakeProjectionXy(itemtoadd, i) and i[1] +i[4] > maxBound[0]:
            neweps.append((itemtoadd[1] + itemtoadd[4], i[0] + i[3], itemtoadd[2]))
            maxBound[0] = i[0] + i[3]

        if CanTakeProjectionXy(itemtoadd, i) and i[2] + i[5] > maxBound[1]:
            neweps.append((itemtoadd[0] + itemtoadd[3], itemtoadd[1], i[2] + i[5]))
            maxBound[1] = i[0] + i[3]

        if CanTakeProjectionZx(itemtoadd, i) and i[0] + i[3] > maxBound[4]:
            neweps.append((i[0] + i[3], itemtoadd[1], itemtoadd[2] + itemtoadd[5]))
            maxBound[4] = i[0] + i[3]

        if CanTakeProjectionZy(itemtoadd, i) and i[0] + i[0] > maxBound[5]:
            neweps.append((itemtoadd[0], i[1] + i[4], itemtoadd[2] + itemtoadd[5]))
            maxBound[5] = i[1] + i[4]
        for EP in neweps:
            DEPL.append(EP)
        DEPL = list(dict.fromkeys(DEPL))
        DEPL = list(sortieralgorithmen.sortZYX(DEPL))
        return DEPL


def EP_First_Fit(items, bin_size, EPL, feasibleSolution):
    for n, i in enumerate(items):
        #bei erster Iteration
        if n == 0 and feasibleSolution == [[]]:
            feasibleSolution[0].append([0, 0, 0, i[0], i[1], i[2]])
            EPL.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
        else:
            nep = guetefunktionen.determinePlacementPoint(feasibleSolution, i, bin_size, EPL)
            if nep is not None:
                nitem = [nep[0][0], nep[0][1], nep[0][2], i[0], i[1], i[2]]
                feasibleSolution[nep[1]].append(nitem)
                EPL[nep[1]] = update3DEPL(nitem, EPL[nep[1]], feasibleSolution[nep[1]], nep[0])
                EPL[nep[1]].remove(nep[0])
            if nep is None:
                feasibleSolution.append([[0, 0, 0, i[0], i[1], i[2]]])
                EPL.append([(i[0], 0, 0), (0, i[0], 0), (0, 0, i[0])])
    return feasibleSolution, EPL


def EP_Best_FitbyVolume(items, bin_size, EPL, feasibleSolution):
    for n, i in enumerate(items):
        packed = 0
        #bei erster Iteration
        if n == 0 and feasibleSolution == [[]]:
            feasibleSolution[0].append([0, 0, 0, i[0], i[1], i[2]])
            EPL.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
        else:
            nep = guetefunktionen.determinePlacementPointLeastFreeVolume(feasibleSolution, i, bin_size, EPL)
            if nep is not None:
                nitem = [nep[0][0], nep[0][1], nep[0][2], i[0], i[1], i[2]]
                feasibleSolution[nep[1]].append(nitem)
                update3DEPL(nitem, EPL[nep[1]], feasibleSolution[nep[1]], nep[0])
                EPL[nep[1]].remove(nep[0])
            if nep is None:
                feasibleSolution.append([[0, 0, 0, i[0], i[1], i[2]]])
                EPL.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
    return feasibleSolution, EPL


def EP_Best_FitbyResidualSpace(items, bin_size, EPL, feasibleSolution):
    for n, i in enumerate(items):
        packed = 0
        #bei erster Iteration
        if n == 0 and feasibleSolution == [[]]:
            feasibleSolution[0].append([0, 0, 0, i[0], i[1], i[2]])
            EPL.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
        else:
            indexofbin, nep = guetefunktionen.determineMaxResPlacementPoint(i, EPL, bin_size, feasibleSolution)
            if nep is not None:
                nitem = [nep[0], nep[1], nep[2], i[0], i[1], i[2]]
                feasibleSolution[indexofbin].append(nitem)
                update3DEPL(nitem, EPL[indexofbin], feasibleSolution[indexofbin], nep)
                EPL[indexofbin].remove(nep)
            if nep is None:
                feasibleSolution.append([[0, 0, 0, i[0], i[1], i[2]]])
                EPL.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
    return feasibleSolution, EPL


def EPWorstFitByResidualSpace(items, bin_size, EPL, feasibleSolution):
    for n, i in enumerate(items):
        packed = 0
        # bei erster Iteration
        if n == 0 and feasibleSolution == [[]]:
            feasibleSolution[0].append([0, 0, 0, i[0], i[1], i[2]])
            EPL.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
        else:
            indexofbin, nep = guetefunktionen.determineLeastResPlacementPoint(i, EPL, bin_size, feasibleSolution)
            if nep is not None:
                nitem = [nep[0], nep[1], nep[2], i[0], i[1], i[2]]
                feasibleSolution[indexofbin].append(nitem)
                update3DEPL(nitem, EPL[indexofbin], feasibleSolution[indexofbin], nep)
                EPL[indexofbin].remove(nep)
            if nep is None:
                feasibleSolution.append([[0, 0, 0, i[0], i[1], i[2]]])
                EPL.append([(i[0], 0, 0), (0, i[1], 0), (0, 0, i[2])])
    return feasibleSolution
