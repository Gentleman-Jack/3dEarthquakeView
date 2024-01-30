import os
import datetime
import sys
import argparse
from operator import itemgetter
from PyQt5 import QtCore

PATH = "Desktop"
FILENAME = "balls.txt"

months = {"JAN":1, "FEB":2, "MAR":3, "APR":4, "MAY":5, "JUN":6, "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}

#auth h class dimiourgeitai gia na boroume na ekpempsoume signals gia to filtro kai thn taksinomish
class statusObject(QtCore.QObject):
    statusMessage = QtCore.pyqtSignal(str, int)

helpSignal = statusObject()


boundriesY = (34.73, 41.80) #lat (31.01, 43.99)
boundriesX = (19.29, 28.30) #lon (15.01, 32.99)

centerY = (boundriesY[0] + boundriesY[1])/2
centerX = (boundriesX[0] + boundriesX[1])/2

stepX = (boundriesX[1] - boundriesX[0])/20
stepY = (boundriesY[1] - boundriesY[0])/20

def latLonToCart(lat, lon):
    retY = (lat-centerY)/stepY
    retX = (lon-centerX)/stepX

    return retX, retY 


def windowToLatLon(w, h, posX, posY):
    lat = round((2*(centerY-boundriesY[1])/h * posY) + boundriesY[1], 2)
    lon = round((-2*(centerX-boundriesX[1])/w * posX) + boundriesX[0], 2)

    return lat, lon


def lineConvertToTuple(line):
    if line[0] == " ":
        line = line[1:]
    time = line[0:22] # 0 - 21 einai olh h hmerominia kai wra xwris to dekadiko twn sec ( prepei ta sec na exoun 2 psifia opwsdipote

###########################################
#    print("time = {}\nlength={}".format(time, len(time)))

#    try:
#        if time[-1] == " ":
#            time = time[:-1] + "0"
#        elif time[-1] == ".":
#            time = time[:-1]
#    except:
#        print("time = {}\nlength={}\nline:{}\nlineLength{}".format(time, len(time), line, len(line)))
#        return
 
    #yparxei lathos se kapoious seismous, sta deuterolepta deixnei 60
#    if time[-2:] == "60":
#        time = time[:-2] + "59"

#    print(time)
#    dt = datetime.datetime.strptime(time, '%Y %b %d %H %M %S')
############################################

    year = int(time[0:4])
    month = months[time[5:8]]
    day = int(time[9:11])
    hour = int(time[14:16])
    minute = int(time[17:19])

    if time[20:22] == "  ":
        second = 0
    elif time[20:22] == "60":
        second = 59
    else:
        second = int(time[20:22])
    dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second) 



    lat = float(line[27:33])
    lon = float(line[35:41])
    # ypodekaplasiazoume to depth gia na exoume ena pio periorismeno euros vathwn
    depth = int(line[42:45])
 #   print("depth = {} depth before = {}".format(depth, depth*10))
    mag = float(line[54:57])

#    x, y = latLonToCart(lat,lon)

    tup = (dt, lat, lon, depth, mag)#, x, y)
    return tup




def choose(data, sortBy=0, descending=False, total=None, minDate=None, maxDate=None, minLat=None, maxLat=None, minLon=None, maxLon=None, minDepth=None, maxDepth=None, minMag=None,maxMag=None):
#    print("Date:", minDate)
    display = []

    if minDate:
        minDate = datetime.datetime.strptime(minDate, '%d/%m/%Y')
#        print("Date converted:", minDate)

    if maxDate:
        maxDate = datetime.datetime.strptime(maxDate, '%d/%m/%Y')

    # ean yparxei filtro efarmose to
    if (minDate or maxDate or minLat or maxLat or minLon or maxLon or minDepth or maxDepth or minMag or maxMag):
        helpSignal.statusMessage.emit("Filtering data", 0)
        for d in data:

            # Den simptisoume tis 2 if se mia gia na yparxei h dynatothta na exoume ena mono orio dhladh mono pros ta pano h mono pros ta kato
            if minDate:
                if d[0] < minDate:
#                    print("Less Date to check{0} date to comparewith{1} result={2}".format(d[0], minDate, d[0] < minDate))
                    continue
            if maxDate:
                if d[0] > maxDate:
#                    print("More Date to check{0} date to comparewith{1} result={2}".format(d[0], maxDate, d[0] > minDate))
                    continue
            if minLat:
                if d[1] < minLat:
                    continue

            if maxLat:
                if d[1] > maxLat:
                    continue

            if minLon :
                if d[2] < minLon:
                        continue

            if maxLon:
                if d[2] > maxLon:
                        continue
                    
            if minDepth:
                if d[3] < minDepth:
                    continue
            if maxDepth:
                if d[3] > maxDepth:
                    continue
            if minMag:
                if d[4] < minMag:
                    continue

            if maxMag:
                if d[4] > maxMag:
                    continue

            display.append(d)
    else:
        display = data

    if sortBy!= 5:
        helpSignal.statusMessage.emit("Sorting data", 0)
        display=sorted(display, key=itemgetter(sortBy), reverse=descending)
#        print("sortBy{0} \n sorted list {1}".format(sortBy,display))
    if total:
        display = display[:total]

    return display


def readData(inputPath=PATH, inputFilename=FILENAME):
    l = []
    #os.path.join used to be flexible to navigate in different OS(windows - Linux - OSX)
    f = open(inputFilename, 'r')#os.path.join(inputPath, inputFilename)

    #skip the first two lines as they are titles
    f.readline()
    f.readline()

    # go through all lines
    for line in f.readlines():
#        print(len(line))
        if len(line) == 1:
            continue
    # make a list of tuples(date, lat, lon, depth, magnitude)
        l.append(lineConvertToTuple(line))
    return l#choose(l, minLat=34.00, minLon=22.32, maxLat=35.79, maxLon =27.80, minMag=6, maxMag=7.0, descending = True)


def parseArguments():
    parser = argparse.ArgumentParser(description="Πρόγραμμα απεικόνησης σεισμών σε τριδιάστατο περιβάλλον")
    parser.add_argument("-s", "--sequential", action="store_true", help="Διαδοχική απεικόνηση σεισμών")
    parser.add_argument("-f", "--file", type=str, help="Αρχείο σεισμών")
    parser.add_argument("--verbose", action="store_true", help="Ένδειξη πληροφοριων σεισμών")

    choicesGroup = parser.add_argument_group("choices", description="Κριτηρια επιλογης σεισμων")
    choicesGroup.add_argument("-sb", "--sortBy", type=int, choices=range(5), default=0, help="Ταξινόμηση κατά 0:Date 1:Lat 2:Lon 3:Depth 4:Mag")
    choicesGroup.add_argument("-d", "--descending", action="store_true", help="φθείνουσα ταξινόμηση")
    choicesGroup.add_argument("-fdt", "--minDate", type=str, help="dd/mm/yyyy")
    choicesGroup.add_argument("-tdt", "--maxDate", type=str, help="dd/mm/yyyy")
    choicesGroup.add_argument("-fd", "--minDepth", type=float, help="float")
    choicesGroup.add_argument("-td", "--maxDepth", type=float, help="float") 
    choicesGroup.add_argument("-fm", "--minMag", type=float, help="float")
    choicesGroup.add_argument("-tm", "--maxMag", type=float, help="float")
    choicesGroup.add_argument("-flat", "--minLat", type=float, help="float")
    choicesGroup.add_argument("-tlat", "--maxLat", type=float, help="float")
    choicesGroup.add_argument("-flon", "--minLon", type=float, help="float")
    choicesGroup.add_argument("-tlon", "--maxLon", type=float, help="float")
    args = parser.parse_args()
#   print (args)
    return args

if __name__ == "__main__":
#    main()

    print(readData())