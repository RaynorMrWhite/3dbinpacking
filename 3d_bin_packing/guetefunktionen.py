import copy


# checks for every Point if item is not bigger than bin
def itemfitsinbin(item, bin_size, placementpointlist):
    for point in placementpointlist:
        for i in range(3):
            if point[i]+item[i] > bin_size:
                return False
    return True


# checks for every item in bin if the new would overlap with one
def checkifitemsoverlap(bin, item, placementpoint):
    for b in bin:
        if b[0]+b[3] < item[0] or b[1]+b[4] < item[1] or b[2]+b[5] < item[2] \
                or placementpoint[0]+item[0] < b[0] or placementpoint[1]+item[1] < b[1]\
                or placementpoint[2]+item[2] < b[2]:
            return False
    return True


# searches the first point on which a item can be packed
def determinePlacementPoint(feasibleSolution, item, bin_size, PlacementPointList):
    for indexofbin, bin in enumerate(feasibleSolution):
        for placementpoint in PlacementPointList[indexofbin]:
            if placementpoint[0] + item[0] <= bin_size and placementpoint[1] + item[1] <= bin_size\
                    and placementpoint[2] + item[2] <= bin_size and checkifitemsoverlap(bin, item, placementpoint):
                return placementpoint, indexofbin
    return None


# returns index of bin with least volume after packing the item
def freeVolumeAfterAccomodation(itemtoadd, bin, binsize):
    volumebin = binsize**3
    for item in bin:
        volumebin -= item[3]*item[4]*item[5] - itemtoadd[0] * itemtoadd[1] * itemtoadd[2]
    return volumebin


# returns index of bin with the least free volume after placing an item
def findIndexOfBinWithLeastFreeVolume(itemtoadd, packedbins, binsize):
    maxfreevolumebinindex = 0
    for bin in packedbins:
        if maxfreevolumebinindex > freeVolumeAfterAccomodation(itemtoadd, bin, binsize):
            maxfreevolumebinindex = packedbins.index(bin)
    return maxfreevolumebinindex


# returns index of bin for the placementpoint structure of placementpointlist = packedbins
def findBinIndexOfPlacementPoint(placementpointlist, placementpoint):
    for indexofbin, binpointlist in enumerate(placementpointlist):
        if placementpoint in binpointlist:
            return indexofbin


# finds first point in which the item can be placed by decreasing volume of bin
def determinePlacementPointLeastFreeVolume(feasibleSolution, item, bin_size, PlacementPointList):
    packedbins = feasibleSolution.copy()
    placementpoints = PlacementPointList.copy()
    while packedbins:
        indexofbin = findIndexOfBinWithLeastFreeVolume(item, packedbins, bin_size)
        for placementpoint in placementpoints[indexofbin]:
            if placementpoint[0] + item[0] <= bin_size and placementpoint[1] + item[1] <= bin_size\
                    and placementpoint[2] + item[
               2] <= bin_size and checkifitemsoverlap(packedbins[indexofbin], item, placementpoint):
                return placementpoint, findBinIndexOfPlacementPoint(PlacementPointList, placementpoint)
        packedbins.remove(packedbins[indexofbin])
        placementpoints.remove(placementpoints[indexofbin])
    return None


# returns optimal point defined by residualspace
def determineMaxResPlacementPoint(itemtoadd, PointList, binsize, feasibleSol):
    placementpoint = copy.deepcopy(PointList)
    while placementpoint != "end":
        indofBin, optPoint = \
            maxResidualSpacePlacementPoint(itemtoadd, placementpoint, binsize)
        if optPoint != ():
            if optPoint[0]+itemtoadd[0] <= binsize and \
                    optPoint[1] + itemtoadd[1] <= binsize\
                    and optPoint[2] + itemtoadd[2] <= binsize and\
            checkifitemsoverlap(feasibleSol[indofBin], itemtoadd, optPoint):
                return indofBin, optPoint
            else:
                placementpoint[indofBin].remove(optPoint)
        else:
            placementpoint = "end"
    return None, None


# finds point within bin with maximum taken Residual Space
def maxResidualSpacePlacementPoint(itemtoadd, placementpointlist, binsize):
    residualspaceEP = 0
    placementpoint = ()
    indexofbin=0
    for i, pointlist in enumerate(placementpointlist):
        for point in pointlist:
            if residualspaceEP < binsize-point[0]-itemtoadd[0] + \
                    binsize-point[1]-itemtoadd[1] + \
                    binsize-point[2]-itemtoadd[2]:
                residualspaceEP = binsize-point[0]-itemtoadd[0] + \
                                  binsize-point[1]-itemtoadd[1] +\
                                  binsize-point[2]-itemtoadd[2]
                placementpoint = point
                indexofbin=i
    return indexofbin, placementpoint


# testingfunction
def listofvolumes(itemtoadd, bins):
    binv=[]
    for b in bins:
        v = 100**3
        for bin in b:
            v -= bin[0] * bin[1] * bin[2] - \
                 itemtoadd[0] * itemtoadd[1] * itemtoadd[2]
        binv.append(v)
    return binv

#print(([13,22,15], [[(39, 0, 0), (0, 85, 0), (0, 0, 72), (39, 85, 0), (0, 85, 72), (39, 0, 39), (39, 85, 72), (39, 10, 0), (39, 0, 21)], [(39, 0, 0), (0, 39, 0), (0, 0, 39), (39, 85, 0), (0, 85, 72), (39, 0, 39), (39, 85, 72)], [(11, 0, 0), (0, 11, 0), (0, 0, 11), (11, 84, 0), (0, 84, 96), (11, 0, 11), (11, 84, 96)]], 100))
#print(listofvolumes([13,22,15],[[(39, 0, 0), (0, 85, 0), (0, 0, 72), (39, 85, 0), (0, 85, 72), (39, 0, 39), (39, 85, 72), (39, 10, 0), (39, 0, 21)], [(39, 0, 0), (0, 39, 0), (0, 0, 39), (39, 85, 0), (0, 85, 72), (39, 0, 39), (39, 85, 72)], [(11, 0, 0), (0, 11, 0), (0, 0, 11), (11, 84, 0), (0, 84, 96), (11, 0, 11), (11, 84, 96)]]))
