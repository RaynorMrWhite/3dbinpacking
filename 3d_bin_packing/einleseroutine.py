import csv


# returns data of csv as [x,y,z] for placementpoints
def openCSV(datei):
    with open(datei, newline='') as csvfile:
        listeItems = [[]]
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for ind, row in enumerate(reader):
            if ind == 0:
                count = 0
            elif ind == 1:
                rowlength = int(row[0])+2
                binsize = int(row[1])
                count += 1
            elif ind % rowlength-1 == 0:
                count += 1
                listeItems.append([])
            elif ind % rowlength != 0:
                listeItems[count-1].append([int(row[0]), int(row[1]), int(row[2])])
    return listeItems, binsize
