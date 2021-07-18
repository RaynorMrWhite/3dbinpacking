import random

def deleteRandomBin(numberofBins, itemlist, feasibleSolution, PlacementPointlist):
    for i in range(numberofBins):
        randomBin = random.randint(0, len(feasibleSolution))
        for i in feasibleSolution[randomBin-1]:
            itemlist.append([i[3], i[4], i[5]])
        del feasibleSolution[randomBin-1]
        del PlacementPointlist[randomBin-1]
    return itemlist
