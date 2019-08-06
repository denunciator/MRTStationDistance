import requests
import json
import time


class StationClass:
    code = ""
    name = ""
    line = ""
    isMRT = 1
    lat = ""
    lon = ""

    def __init__(self, inString):
        self.code, self.name, self.line, self.isMRT, self.lat, self.lon = inString.split(",")
        if self.lon[-1] == "\n":
            self.lon = self.lon[0:-1]

'''WRITE YOUR API KEY IN'''
accessKey = ""

baseUrl = "https://developers.onemap.sg"


'takes a list of train stations from LTA DataMall, with the Chinese columns removed'
trainStationsList = list(open('./train stations.csv', 'r'))[1:]

'''Generating the coordinates for the stations and writing them to file'''
'open file and blank if it exists, create if it does not'
outFile = open("stationGPS.txt", "w+")
outFile.truncate(0)
outFile.write("StationCode,StationName,StationLine,StationIsMrt,Latitude,Longitude\n")

for stations in trainStationsList:
    stationCode, stationName, stationLine, stationIsMrt = stations.split(",")
    stationIsMrt = stationIsMrt[0]

    response = requests.get(baseUrl + "/commonapi/search?searchVal=" + stationName + "+" + stationCode + "&returnGeom=Y&getAddrDetails=N")
    if stationCode == "PTC":
        response = requests.get(baseUrl + "/commonapi/search?searchVal=NE17&returnGeom=Y&getAddrDetails=N")

    aPyObj = json.loads(response.content)
    print(stationCode + stationName)
    stationLat = aPyObj["results"][0]["LATITUDE"]
    stationLon = aPyObj["results"][0]["LONGITUDE"]

    outFile.write(stationCode + "," + stationName + "," + stationLine + "," + stationIsMrt + "," + stationLat + "," + stationLon)

    if stations != trainStationsList[-1]:
        outFile.write("\n")


trainStationsList = None
trainStationsList = list(open('stationGPS.txt', 'r'))[1:]

trainDistanceFile = open("stationDistances5.txt", "w+")
trainDistanceFile.truncate(0)
trainDistanceFile.write("StartStationCode,StartStationName,EndStationCode,EndStationName,Distance\n")

for stationStartIter in range(0, len(trainStationsList)-1):
    for stationEndIter in range(stationStartIter+1, len(trainStationsList)):
        if stationStartIter == stationEndIter:
            continue

        startStation = StationClass(trainStationsList[stationStartIter])
        endStation = StationClass(trainStationsList[stationEndIter])

        if startStation.name == endStation.name:
            continue

        requestString = baseUrl + "/privateapi/routingsvc/route?start=" + startStation.lat + "%2C" + startStation.lon + "&end=" + endStation.lat + "%2C" + endStation.lon + "&routeType=pt&token=" + accessKey + "&date=2019-02-26&time=12%3A00%3A00&mode=TRANSIT&maxWalkDistance=1"
        response = requests.get(requestString)
        responseStatus = response.status_code

        if responseStatus != 200:
            print("execution stopped on pairs " + startStation.name + " " + endStation.name + ". Waiting 2s... \n")
            time.sleep(2)
            response = requests.get(requestString)
            responseStatus = response.status_code

        aPyObj = json.loads(response.content)
        aPyObj = aPyObj["plan"]["itineraries"]

        shortestDist = 999999999
        distanceHold = 0

        for i in range(0, len(aPyObj)):
            curItin = aPyObj[i]["legs"]
            for j in range(0, len(curItin)):
                distanceHold += curItin[j]["distance"]

            if shortestDist > distanceHold:
                shortestDist = distanceHold
            distanceHold = 0

        trainDistanceFile.write(startStation.code + "," + startStation.name + "," + endStation.code + "," + endStation.name + "," + str(shortestDist) + "\n")

        startStation = None
        endStation = None
