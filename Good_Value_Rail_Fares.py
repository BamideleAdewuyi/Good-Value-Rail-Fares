import requests
import json
import haversine as hs
from haversine import Unit
import urllib.request
import matplotlib.pyplot as plt
import numpy as np

# Station details request
url = "https://sandbox.fastjp.dev/api/Station"

# This part of the code needs Fast JP API credentials. Details of their API are here: https://www.fastjp.com/Commercial
payload = json.dumps({
  "Login": "LOGIN",
  "Password": "PASSWORD",
  "RetailFilters": "use_rcs=1;rcs_use_flow_management=1;rcs_licensee_type=3RD_PARTY;rcs_sales_channel=WEB;rcs_fulfilment_methods=TOD,ETICKET"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

# Lists for essential information
listOfUic = []
listOfNames = []
listOfLat = []
listOfLong = []
listOfCrs = []
listOfPostcodes = []

# Add UIC
for i in response.json()["list"]:

    if i["uic"] != "":
        listOfUic.append(i["uic"])

# Add name
for i in response.json()["list"]:
    if i["uic"] != "":

        listOfNames.append(i["fullName"]["#cdata-section"])

# Add latitude
for i in response.json()["list"]:
    if i["uic"] != "":

        listOfLat.append(i["latitude"])

# Add longitude
for i in response.json()["list"]:
    if i["uic"] != "":

        listOfLong.append(i["longitude"])

# Add CRS
for i in response.json()["list"]:
    if i["uic"] != "":

        listOfCrs.append(i["crs"])

# Add postcode
for b in response.json()["list"]:
  if b["uic"] != "":

    listOfPostcodes.append(b["address"]["#cdata-section"])

# List of stations with essential information
stationDetails = list(zip(listOfNames, listOfCrs, listOfUic, listOfLat, listOfLong, listOfPostcodes))

# Clear any stations with no postcode
stationDetails = [item for item in stationDetails if item[5] != '']

# List of most used stations Codes
londonMostUIC = ['7014440', '7054260', '7030870', '7061210', '7069650']
scotMostUIC = ['7098130', '7093280']
nEastMostUIC = ['7077280']
yorkMostUIC = ['7084870', '7066910', '7082630']
eMidsMostUIC = ['7018260', '7019470']
eastMostUIC = ['7070220', '7068360']
sEastMostUIC = ['7052680', '7031490']
sWestMostUIC = ['7032310', '7057550']
walesMostUIC = ['7038990', '7036740']
wMidsMostUIC = ['7011270', '7010300']
nWestMostUIC = ['7029680', '7022460']
allMostUIC = ['7014440', '7054260', '7030870', '7061210', '7069650', '7098130', '7093280', '7077280', '7084870', '7066910', '7082630', '7018260', '7019470', '7070220', '7068360', '7052680', '7031490', '7032310', '7057550', '7038990', '7036740', '7011270', '7010300', '7029680', '7022460']

# Lists for station groups
londonMost = []
scotMost = []
nEastMost = []
yorkMost = []
eMidsMost = []
eastMost = []
sEastMost = []
sWestMost = []
walesMost = []
wMidsMost = []
nWestMost = []
allMost = []

# Function for grouping stations
def group(stations, codes, group):
  '''
  Groups stations by region.

  Parameters:
  stations - List containing details of all stations.
  codes - List of the UICs of the stations to be grouped.
  group - Empty list for stations whose UICs match those in codes to be put into.

  Return:
  group - A list of the UICs of the stations grouped in a specific region
  '''
  for station in stations:
    for code in codes:
        if code == station[2]:
          group.append(station)

# Grouping the main stations of each region
# London
group(stationDetails, londonMostUIC, londonMost)

# Scotland
group(stationDetails, scotMostUIC, scotMost)

# North East
group(stationDetails, nEastMostUIC, nEastMost)

# Yorkshire and Humber
group(stationDetails, yorkMostUIC, yorkMost)

# East Midlands
group(stationDetails, eMidsMostUIC, eMidsMost)

# East
group(stationDetails, eastMostUIC, eastMost)

# South East
group(stationDetails, sEastMostUIC, sEastMost)

# South West
group(stationDetails, sWestMostUIC, sWestMost)

# Wales
group(stationDetails, walesMostUIC, walesMost)

# West Midlands
group(stationDetails, wMidsMostUIC, wMidsMost)

# North West
group(stationDetails, nWestMostUIC, nWestMost)

# All
group(stationDetails, allMostUIC, allMost)

# Let user know how program works
print("This program performs 3 functions:\n - It can calculate the value of specified journeys according to certain metrics. \n - It can calculate the best and worst value adult journey according to the same metrics from a specified origin station and budget. \n - It can give a regional comparison of the average adult fares with respect to the same metrics.")
print("The metrics are:\n - Price per mile of track. \n - Price per mile as the crow flies. \n - Price per minute of journey. \n - Price per minute saved by travelling by train, rather than by car.")

# Initial Function select
functionSelect = 2

# Set while loop
while functionSelect != 0:
    
    try:
        # Select the function
        functionSelect = int(input("Press 1 for journey value metrics, 2 for best value journeys from a selected origin, 3 for regional comparison. Press 0 to quit. "))

        # Get the journey metrics
        if functionSelect == 1:

            try:
                # Select origin, destination and number of passengers
                origin = str(input("Enter CRS code for origin station "))
                dest = str(input("Enter CRS code for destination station "))
                numAdult = int(input("Enter number of adults "))
                numChild = int(input("Enter number of children "))

                # UICs for journey
                journey = []

                # Latitude and Longitude for journey
                latLongFrom = []
                latLongTo = []

                # Add uic and lat/long for selected stations
                for j in stationDetails:
                    if j[1].casefold() == origin.casefold():
                        print("Journey origin:", j[0])
                        journey.append(j[2])
                        latLongFrom.append(j[3])
                        latLongFrom.append(j[4])

                for p in stationDetails:
                    if p[1].casefold() == dest.casefold():
                        print("Journey destination:", p[0])
                        journey.append(p[2])
                        latLongTo.append(p[3])
                        latLongTo.append(p[4])


                # If a journey can be found
                if len(journey) == 2:

                    # Getting car routes
                    # This part of the code requires TomTom routing API credentials. These can be created at https://developer.tomtom.com/user/login
                    url="https://api.tomtom.com/routing/1/calculateRoute/"+str(latLongFrom[0])+","+str(latLongFrom[1])+":"+str(latLongTo[0])+","+str(latLongTo[1])+"/json?maxAlternatives=3"+\
                        "&routeRepresentation=polyline&computeTravelTimeFor=all&traffic=false&avoid=unpavedRoads&key=API KEY"
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req) as tomTomResponse:

                        the_page = (tomTomResponse.read())
                        json_string = the_page.decode('utf-8')
                        data=json.loads(json_string)
                        
                        # List for car travel times
                        times = []

                        # Finding routes
                        routes = data['routes']
                        for route in routes:
                            summary = route['summary']
                            times.append(route['summary']["travelTimeInSeconds"])

                    # Getting train journey details
                    journeyPlanUrl = "https://sandbox.fastjp.dev/api/JourneyPlanner/"

                    # This part of the code needs Fast JP API credentials. Details of their API are here: https://www.fastjp.com/Commercial
                    payload = json.dumps({
                    "OutboundJourney": {
                        "FromUICs": [
                        journey[0]
                        ],
                        "ToUICs": [
                        journey[1]
                        ],
                        "SearchStartTime": "2022-11-15T10:00:00",
                        "ArriveBefore": 0,
                        "SearchLength": 30,
                        "ExtraInterchangeTime": 0,
                        "MaxChanges": 99,
                        "IncludedTravelModes": {
                        "Train": 1,
                        "Bus": 1,
                        "Tube": 1,
                        "Metro": 1,
                        "Walk": 1,
                        "Transfer": 1,
                        "Ship": 0,
                        "SuppressInitialFixedLinks": 0
                        },
                        "IncludedTOCs": [],
                        "ExcludedTOCs": [],
                        "IncludedUICs": [],
                        "ExcludedUICs": [],
                        "IncludedUICsProcessInOrder": 0,
                        "IncludedTrains": None,
                        "ExcludedTrains": None,
                        "ForceFareOrigin": 0,
                        "ForceFareDestination": 0
                    },
                    "ReturnJourney": {},
                    "ExcludeFares": 0,
                    "IncludeSplitFares": 0,
                    "NumAdults": numAdult,
                    "NumChildren": numChild,
                    "Login": {
                        "Login": "LOGIN",
                        "Password": "PASSWORD",
                        "RequiredVersion": "",
                        "RetailFilters": "use_rcs=1;rcs_use_flow_management=1;rcs_licensee_type=TOC;rcs_sales_channel=WEB;rcs_fulfilment_methods=ETICKET,TOD;",
                        "NRSProxy": None
                    },
                    "AdvanceLoad": 1,
                    "AdvanceAvailability": 1,
                    "SearchType": 0,
                    "MinimumLayover": -1,
                    "ZonalMergeMode": 1,
                    "NonZonalMergeMode": 1,
                    "AllowStepBack": 0,
                    "IgnoreItinerariesInPast": 0
                    })
                    headers = {
                    'Content-Type': 'application/json'
                    }

                    journeyResponse = requests.request("POST", journeyPlanUrl, headers=headers, data=payload)

                    # If there are outbound journeys available
                    if journeyResponse.json()["outboundJourneys"] != [] and journeyResponse.json()["fares"] != None:
                        # Getting fares
                        fareList = []

                        for i in journeyResponse.json()["fareDetails"]:
                            if i["ticketCode"] == "SDS" or i["ticketCode"] == "SOS":
                                fareList.append(i["price"])

                        # Finding max fare
                        fare = max(fareList)/100
                        print("")
                        print("The fare for this journey is","£{:.2f}".format(fare))

                        # Getting mileage
                        for j in journeyResponse.json()["fares"]:
                            if "outMileage" in j:
                                mileageDict = j

                        # Best car time
                        bestCarTime = round(min(times)/60)

                        #Train journey duration
                        trainTime = journeyResponse.json()["outboundJourneys"][0]["journeyLength"]

                        # Miles of track
                        outMileage = mileageDict["outMileage"]/100

                        # Miles as crow flies
                        crowFliesDist = hs.haversine(latLongFrom,latLongTo, unit=Unit.MILES)

                        # Price per mile of track
                        if outMileage != 0:
                            pricePerMile = "£{:.2f}".format(fare/outMileage)
                        
                        # Price per crow flies mile
                        pricePerCrowFliesMile = "£{:.2f}".format(fare/crowFliesDist)

                        # Price per minute of train journey
                        pricePerMinTrain = "£{:.2f}".format(fare/trainTime)

                        # How much time saved by using the train
                        timeSaved = bestCarTime - trainTime

                        # If there is time saved
                        if timeSaved > 0:
                            # Find the cost per minute saved
                            pricePerMinSaved = "£{:.2f}".format(fare/timeSaved)
                        else:
                            pricePerMinSaved = "There is no time saved by travelling by train, rather than car."

                        if outMileage != 0:
                            print("The journey is", outMileage, "miles of track and costs", pricePerMile, "per mile.")
                        else:
                            print("There are no miles covered on national rail for this journey.")
                            print("")

                        # Return the value of the journey
                        print("The journey is", "{:.2f}".format(crowFliesDist), "miles as the crow flies and costs", pricePerCrowFliesMile, "per mile.")
                        print("The journey takes", bestCarTime, "minutes by car.")
                        print("The journey takes", trainTime, "minutes by train.")
                        print("The journey costs", pricePerMinTrain, "per minute of train journey.")
                        print("Price per minute saved by travelling by train:", pricePerMinSaved)
                        print("")

                    else:
                        print("There are no national rail journeys available between these stations.")

                # If a journey cannot be found
                else:
                    print("You must enter valid CRS code.")
            
            except ValueError:
                print("You did not enter a number.")
                
        # Get the best value trips
        elif functionSelect == 2:

            try:

                # Enter CRS of origin station
                origin = str(input("Enter the CRS of your origin station "))

                # Budget in pounds
                budg = float(input("Enter your budget in pounds "))

                # Let user know that the metrics are being calculated
                print("Calculating...")

                # Latitude and Longitude for journey
                latLongFrom = []

                # List of affordable journeys
                posJourneys = []

                # Get the origin CRS and latitude and longitude
                for stat in stationDetails:
                    # for s in stat:
                    if stat[1].casefold() == origin.casefold():
                        org = stat[2]
                        latLongFrom.append(stat[3])
                        latLongFrom.append(stat[4])

                # Calculate all possible fares
                for stat in stationDetails:
                    if stat[1].casefold() != origin.casefold():

                        # Getting journey details
                        journeyPlanUrl = "https://sandbox.fastjp.dev/api/JourneyPlanner/"

                        # This part of the code needs Fast JP API credentials. Details of their API are here: https://www.fastjp.com/Commercial
                        payload = json.dumps({
                        "OutboundJourney": {
                            "FromUICs": [
                            org
                            ],
                            "ToUICs": [
                            stat[2]
                            ],
                            "SearchStartTime": "2022-11-15T10:00:00",
                            "ArriveBefore": 0,
                            "SearchLength": 1,
                            "ExtraInterchangeTime": 0,
                            "MaxChanges": 99,
                            "IncludedTravelModes": {
                            "Train": 1,
                            "Bus": 1,
                            "Tube": 1,
                            "Metro": 1,
                            "Walk": 1,
                            "Transfer": 1,
                            "Ship": 0,
                            "SuppressInitialFixedLinks": 0
                            },
                            "IncludedTOCs": [],
                            "ExcludedTOCs": [],
                            "IncludedUICs": [],
                            "ExcludedUICs": [],
                            "IncludedUICsProcessInOrder": 0,
                            "IncludedTrains": None,
                            "ExcludedTrains": None,
                            "ForceFareOrigin": 0,
                            "ForceFareDestination": 0
                        },
                        "ReturnJourney": {},
                        "ExcludeFares": 0,
                        "IncludeSplitFares": 0,
                        "NumAdults": 1,
                        "NumChildren": 0,
                        "Login": {
                            "Login": "LOGIN",
                            "Password": "PASSWORD",
                            "RequiredVersion": "",
                            "RetailFilters": "use_rcs=1;rcs_use_flow_management=1;rcs_licensee_type=TOC;rcs_sales_channel=WEB;rcs_fulfilment_methods=ETICKET,TOD;",
                            "NRSProxy": None
                        },
                        "AdvanceLoad": 1,
                        "AdvanceAvailability": 1,
                        "SearchType": 0,
                        "MinimumLayover": -1,
                        "ZonalMergeMode": 1,
                        "NonZonalMergeMode": 1,
                        "AllowStepBack": 0,
                        "IgnoreItinerariesInPast": 0
                        })
                        headers = {
                        'Content-Type': 'application/json'
                        }

                        journeyResponse = requests.request("POST", journeyPlanUrl, headers=headers, data=payload)

                        # Create empty list of possible fares
                        fareList = []

                        # Destination lat long
                        latLongTo = [stat[3], stat[4]]
                        if journeyResponse.json()["outboundJourneys"] != [] and journeyResponse.json()["fares"] != None:
                            # Getting fares
                            for i in journeyResponse.json()["fareDetails"]:
                                if i["ticketCode"] == "SDS" or i["ticketCode"] == "SOS":
                                    # Add fares to list
                                    fareList.append(i["price"])

                                    # Get miles of track for each affordable journey
                                    for c in journeyResponse.json()["fares"]:
                                        mileage = (c["outMileage"])                       

                            # Find best value per crow flies mile
                            crowFliesDist = hs.haversine(latLongFrom,latLongTo, unit=Unit.MILES)

                            # Find train times
                            trainTime = journeyResponse.json()["outboundJourneys"][0]["journeyLength"]

                        else:
                            None
                     
                        # Add affordable journeys to list
                        if len(fareList) > 0 and max(fareList)/100 <= budg and mileage > 0:
                            # Add the station name, fare, mileages, crow flies distance, journey duration and latitude/longitude
                            posJourneys.append([stat[0], max(fareList)/100, mileage/100, crowFliesDist, trainTime, stat[3], stat[4]])

                # If there are journeys within the budget
                if posJourneys != []:
                    
                    # Initial metric value
                    metric = 2

                    # Set while loop so it is possible to check different metrics for the same origin and budget
                    while metric != 0:

                        try:
                            # Select metric
                            metric = int(input("Press 1 for the best and worst value journey per mile of track, 2 for mile as crow flies, 3 for value per minute of journey, 4 for value per minute saved, or 0 to restart program. "))
                            
                            # For best journey per mile of track
                            if metric == 1:
                                # List of best value journeys
                                valTrack = []

                                # Add all costs per mile of track to list
                                for journ in posJourneys:
                                    valTrack.append(journ[1]/journ[2])                     
                                
                                # Find the index of each minimum and maximum value in the value list
                                # Set count to -1
                                count = -1
                                # List for indices of each min and max value
                                bestI = []
                                worstI = []

                                # Add the index of each min and max value to the lists
                                for val in valTrack:
                                    count += 1
                                    if val == min(valTrack):
                                        # Add the index to the best value list if value is min
                                        bestI.append(count)
                                    if val == max(valTrack):
                                        # Add the index to the worst value list if the value is max
                                        worstI.append(count)
                                
                                # List of best and worst value journeys
                                bestJourneys = []
                                worstJourneys = []

                                # For indices in bestI
                                for num in bestI:
                                    # From the possible journeys, add these indices
                                    bestJourneys.append(posJourneys[num])
                                
                                # For indices in worstI
                                for num in worstI:
                                    # From the possible journeys, add these indices
                                    worstJourneys.append(posJourneys[num])
                                
                                # Print space
                                print("")

                                # Return the best value journeys
                                for j in bestJourneys:
                                    print("Best value journey is to:", j[0], "and the fare is", "£{:.2f}".format(j[1]),". The journey is ", j[2], "miles of track and costs", "£{:.2f}".format(j[1]/j[2]), "per mile.")
                                
                                # Return the worst value journeys
                                for i in worstJourneys:
                                    print("Worst value journey is to:", i[0], "and the fare is", "£{:.2f}".format(i[1]),". The journey is ", i[2], "miles of track and costs", "£{:.2f}".format(i[1]/i[2]), "per mile.")

                                # Print space
                                print("")

                            # Best value per mile as crow flies         
                            elif metric == 2:
                                # List of best value journeys
                                valCrow = []
                                for journ in posJourneys:
                                    valCrow.append(journ[1]/journ[3])
                                
                                # Find the index of each maximum and minimum value in the value list
                                # Set count to -1
                                count = -1
                                # List for indices of each max and min value
                                bestI = []
                                worstI = []

                                # Add the index of each min and max value to the lists
                                for val in valCrow:
                                    count += 1
                                    if val == min(valCrow):
                                        # Add the index to the best value list if value is min
                                        bestI.append(count)
                                    if val == max(valCrow):
                                        # Add the index to the worst value list if the value is max
                                        worstI.append(count)

                                # List of best and worst value journeys
                                bestJourneys = []
                                worstJourneys = []

                                # For indices in bestI
                                for num in bestI:
                                    # From the possible journeys, add these indices
                                    bestJourneys.append(posJourneys[num])

                                # For indices in worstI
                                for num in worstI:
                                    # From the possible journeys, add these indices
                                    worstJourneys.append(posJourneys[num])

                                # Print space
                                print("")

                                # Return the best value journeys
                                for f in bestJourneys:
                                    print("Best value journey is to:", f[0], "and the fare is", "£{:.2f}".format(f[1]),". The journey is", "{:.2f}".format(f[3]), "miles as the crow flies and costs", "£{:.2f}".format(f[1]/f[3]), "per mile.")

                                # Return the worst value journeys
                                for h in worstJourneys:
                                    print("Worst value journey is to:", h[0], "and the fare is", "£{:.2f}".format(h[1]),". The journey is", "{:.2f}".format(h[3]), "miles as the crow flies and costs", "£{:.2f}".format(h[1]/h[3]), "per mile.")

                                # Print space
                                print("")

                            # Best journey per minute of duration
                            elif metric == 3:
                                # List of value of journeys per minute
                                valMin = []
                                for journ in posJourneys:
                                    valMin.append(journ[1]/journ[4])
                                
                                # Find the index of each maximum and minimum value in the value list
                                count = -1
                                # List for indices of each max and min value
                                bestI = []
                                worstI = []

                                # Add the index of each min and max value to the lists
                                for val in valMin:
                                    count += 1
                                    if val == min(valMin):
                                        # Add the index to the best value list if value is min
                                        bestI.append(count)
                                    if val == max(valMin):
                                        # Add the index to the worst value list if the value is max
                                        worstI.append(count)

                                # List of best and worst value journeys
                                bestJourneys = []
                                worstJourneys = []

                                # For indices in bestI
                                for num in bestI:
                                    # From the possible journeys, add these indices
                                    bestJourneys.append(posJourneys[num])
                                
                                # For indices in worstI
                                for num in worstI:
                                    # From the possible journeys, add these indices
                                    worstJourneys.append(posJourneys[num])

                                # Print space
                                print("")

                                # Return the best value journeys
                                for h in bestJourneys:
                                    print("Best value journey is to:", h[0], "and the fare is", "£{:.2f}".format(h[1]),". The journey is", h[4], "minutes long and costs", "£{:.2f}".format(h[1]/h[4]), "per minute.")

                                # Return the worst value journeys
                                for l in worstJourneys:
                                    print("Worst value journey is to:", l[0], "and the fare is", "£{:.2f}".format(l[1]),". The journey is", l[4], "minutes long and costs", "£{:.2f}".format(l[1]/l[4]), "per minute.")

                                # Print space
                                print("")

                            # Best journey per minute saved
                            elif metric == 4:

                                # Let user know that car routes are being calculated
                                print("Calculating car routes...")

                                # Lists for best and worst value journeys
                                bestValSave = []
                                bestSav = []
                                bestI = []
                                worstI = []

                                for journ in posJourneys:
                                    # Getting car routes
                                    # This part of the code requires TomTom routing API credentials. These can be created at https://developer.tomtom.com/user/login
                                    url="https://api.tomtom.com/routing/1/calculateRoute/"+str(latLongFrom[0])+","+str(latLongFrom[1])+":"+str(journ[5])+","+str(journ[6])+"/json?maxAlternatives=3"+\
                                        "&routeRepresentation=polyline&computeTravelTimeFor=all&traffic=false&avoid=unpavedRoads&key=API KEY"
                                    req = requests.get(url, timeout=120)
                                    data = req.json()

                                    # List for travel times
                                    times = [] 

                                    # If there is a route by car
                                    if 'routes' in data:
                                        # Finding routes
                                        routes = data['routes']
                                        for route in routes:
                                            summary = route['summary']
                                            times.append(route['summary']["travelTimeInSeconds"])
                                    else:
                                        times = "There are no possible routes by car."

                                    # Best car time if there is a route
                                    if times != "There are no possible routes by car.":
                                        bestCarTime = round(min(times)/60)
                                
                                        # How much time saved by using the train
                                        timeSaved = bestCarTime - journ[4]
                                    else:
                                        timeSaved = "There are no possible routes by car."

                                    # Find the cost per minute saved and append it to the journey and bestValSaved if there is a route and there is time saved
                                    if timeSaved != "There are no possible routes by car.":
                                        if timeSaved > 0:
                                            pricePerMinSaved = "£{:.2f}".format(journ[1]/timeSaved)
                                            journ.append(pricePerMinSaved)
                                            # Append the destination, price per min saved, best car time, train time and the fare
                                            bestValSave.append([journ[0], pricePerMinSaved, bestCarTime, journ[4], journ[1]])

                                # Make list of savings in order to find the best and worst
                                if bestValSave != []:
                                    for sav in bestValSave:
                                        # Add savings to list
                                        bestSav.append(sav[1])
                                                                
                                # Find the index of each highest and lowest saving in the list
                                count = -1
                                for val in bestSav:
                                    count += 1
                                    # Add the index to the list if it is the highest saving
                                    if val == min(bestSav):
                                        bestI.append(count)
                                    # Add the index to the list if it is the lowest saving
                                    if val == max(bestSav):
                                        worstI.append(count)

                                # Lists of best and worst value journeys
                                bestJourneys = []
                                worstJourneys = []
                                # For indices in bestI
                                for num in bestI:
                                    # From the possible journeys, add these indices
                                    bestJourneys.append(bestValSave[num])
                                
                                # For indices in worstI
                                for num in worstI:
                                    # From the possible journeys, add these indices
                                    worstJourneys.append(bestValSave[num])

                                # Print space
                                print("")

                                # Return the best and worst value journeys if there are any
                                if bestJourneys != []:
                                    for h in bestJourneys:
                                        print("Best value journey is to:", h[0], "and the fare is", "£{:.2f}".format(h[4]),". The journey takes", h[2], "minutes by car and", h[3], "minutes by train. It costs", h[1], "per minute saved.")

                                    for k in worstJourneys:
                                        print("Worst value journey is to:", k[0], "and the fare is", "£{:.2f}".format(k[4]),". The journey takes", k[2], "minutes by car and", k[3], "minutes by train. It costs", k[1], "per minute saved.")
                                else:
                                    print("There are no journeys for which the train is faster than driving.")

                                # Print space
                                print("")

                        # If the user does not enter a number
                        except ValueError:
                            print("You did not enter a number.")
                else:
                    print("There are no journeys available within your budget.")

            # If the user does not enter a valid CRS code
            except NameError:
                print("You did not enter a valid CRS code.")

        # Get a regional comparison
        elif functionSelect == 3:

            # Let user know that metrics are being calculated
            print("Calculating...")

            # Counters for number of journeys
            lonCount = 0
            scotCount = 0
            nEastCount = 0
            yorkCount = 0
            nWestCount = 0
            eMidCount = 0
            wMidCount = 0
            walesCount = 0
            eastCount = 0
            sEastCount = 0
            sWestCount = 0

            # Counters for number of journeys by car
            lonCarCount = 0
            scotCarCount = 0
            nEastCarCount = 0
            yorkCarCount = 0
            nWestCarCount = 0
            eMidCarCount = 0
            wMidCarCount = 0
            walesCarCount = 0
            eastCarCount = 0
            sEastCarCount = 0
            sWestCarCount = 0
            
            # Totals per mile of track
            lonTotPerMile = 0
            scotTotPerMile = 0
            nEastTotPerMile = 0
            yorkTotPerMile = 0
            nWestTotPerMile = 0
            eMidTotPerMile = 0
            wMidTotPerMile = 0
            walesTotPerMile = 0
            eastTotPerMile = 0
            sEastTotPerMile = 0
            sWestTotPerMile = 0

            # Totals per mile as crow flies
            lonTotPerCrow = 0
            scotTotPerCrow = 0
            nEastTotPerCrow = 0
            yorkTotPerCrow = 0
            nWestTotPerCrow = 0
            eMidTotPerCrow = 0
            wMidTotPerCrow = 0
            walesTotPerCrow = 0
            eastTotPerCrow = 0
            sEastTotPerCrow = 0
            sWestTotPerCrow = 0

            # Totals per mile as crow flies
            lonTotPerMin = 0
            scotTotPerMin = 0
            nEastTotPerMin = 0
            yorkTotPerMin = 0
            nWestTotPerMin = 0
            eMidTotPerMin = 0
            wMidTotPerMin = 0
            walesTotPerMin = 0
            eastTotPerMin = 0
            sEastTotPerMin = 0
            sWestTotPerMin = 0

            # Totals per minute saved
            lonTotPerSav = 0
            scotTotPerSav = 0
            nEastTotPerSav = 0
            yorkTotPerSav = 0
            nWestTotPerSav = 0
            eMidTotPerSav = 0
            wMidTotPerSav = 0
            walesTotPerSav = 0
            eastTotPerSav = 0
            sEastTotPerSav = 0
            sWestTotPerSav = 0

            # Iterate over all the most used stations
            for stat in allMost:
                origin = stat[2]

                for s in allMost:
                    if s[2] != origin:
                        journey = [origin, s[2]]
                        latLongFrom = [stat[3], stat[4]]
                        latLongTo = [s[3], s[4]]
                    
                        # Getting train journey details
                        journeyPlanUrl = "https://sandbox.fastjp.dev/api/JourneyPlanner/"

                        # This part of the code needs Fast JP API credentials. Details of their API are here: https://www.fastjp.com/Commercial
                        payload = json.dumps({
                        "OutboundJourney": {
                            "FromUICs": [
                            journey[0]
                            ],
                            "ToUICs": [
                            journey[1]
                            ],
                            "SearchStartTime": "2022-11-15T10:00:00",
                            "ArriveBefore": 0,
                            "SearchLength": 30,
                            "ExtraInterchangeTime": 0,
                            "MaxChanges": 99,
                            "IncludedTravelModes": {
                            "Train": 1,
                            "Bus": 1,
                            "Tube": 1,
                            "Metro": 1,
                            "Walk": 1,
                            "Transfer": 1,
                            "Ship": 0,
                            "SuppressInitialFixedLinks": 0
                            },
                            "IncludedTOCs": [],
                            "ExcludedTOCs": [],
                            "IncludedUICs": [],
                            "ExcludedUICs": [],
                            "IncludedUICsProcessInOrder": 0,
                            "IncludedTrains": None,
                            "ExcludedTrains": None,
                            "ForceFareOrigin": 0,
                            "ForceFareDestination": 0
                        },
                        "ReturnJourney": {},
                        "ExcludeFares": 0,
                        "IncludeSplitFares": 0,
                        "NumAdults": 1,
                        "NumChildren": 0,
                        "Login": {
                            "Login": "LOGIN",
                            "Password": "PASSWORD",
                            "RequiredVersion": "",
                            "RetailFilters": "use_rcs=1;rcs_use_flow_management=1;rcs_licensee_type=TOC;rcs_sales_channel=WEB;rcs_fulfilment_methods=ETICKET,TOD;",
                            "NRSProxy": None
                        },
                        "AdvanceLoad": 1,
                        "AdvanceAvailability": 1,
                        "SearchType": 0,
                        "MinimumLayover": -1,
                        "ZonalMergeMode": 1,
                        "NonZonalMergeMode": 1,
                        "AllowStepBack": 0,
                        "IgnoreItinerariesInPast": 0
                        })
                        headers = {
                        'Content-Type': 'application/json'
                        }

                        journeyResponse = requests.request("POST", journeyPlanUrl, headers=headers, data=payload)

                        # If there are outbound journeys available
                        if journeyResponse.json()["outboundJourneys"] != [] and journeyResponse.json()["fares"] != None:
                            # Getting fares
                            fareList = []
                            for i in journeyResponse.json()["fareDetails"]:
                                if i["ticketCode"] == "SDS" or i["ticketCode"] == "SOS":
                                    fareList.append(i["price"])

                            # If the fare list is not empty
                            if fareList != []:
                                # Finding max fare
                                fare = max(fareList)/100

                                # Getting mileage
                                for j in journeyResponse.json()["fares"]:
                                    if "outMileage" in j:
                                        mileageDict = j

                                # Miles as crow flies
                                crowFliesDist = hs.haversine(latLongFrom,latLongTo, unit=Unit.MILES)

                                # Train journey duration
                                trainTime = journeyResponse.json()["outboundJourneys"][0]["journeyLength"]        

                        # Miles of track
                        outMileage = mileageDict["outMileage"]/100

                        # Getting car routes
                        # This part of the code requires TomTom routing API credentials. These can be created at https://developer.tomtom.com/user/login
                        url="https://api.tomtom.com/routing/1/calculateRoute/"+str(latLongFrom[0])+","+str(latLongFrom[1])+":"+str(latLongTo[0])+","+str(latLongTo[1])+"/json?maxAlternatives=3"+\
                            "&routeRepresentation=polyline&computeTravelTimeFor=all&traffic=false&avoid=unpavedRoads&key=API KEY"
                        req = requests.get(url, timeout=120)
                        data = req.json()

                        # List for travel times
                        times = []

                        # If there is a route by car
                        if 'routes' in data:
                            # Finding routes
                            routes = data['routes']
                            for route in routes:
                                summary = route['summary']
                                times.append(route['summary']["travelTimeInSeconds"])
                        else:
                            times = "There are no possible routes by car."

                        # Best car time if there is a route
                        if times != "There are no possible routes by car.":
                            bestCarTime = round(min(times)/60)
                    
                            # How much time saved by using the train
                            timeSaved = bestCarTime - trainTime
                        else:
                            timeSaved = "There are no possible routes by car."

                        # Find the cost per minute saved, if any and count how many journeys for each region save time
                        if timeSaved != "There are no possible routes by car.":
                            if timeSaved > 0:
                                # Price per minute saved
                                pricePerMinSaved = fare/timeSaved

                                # Check which region journey is from
                                if stat in londonMost:
                                    lonTotPerSav += pricePerMinSaved
                                    lonCarCount += 1

                                elif stat in scotMost:
                                    scotTotPerSav += pricePerMinSaved
                                    scotCarCount += 1
                                
                                elif stat in nEastMost:
                                    nEastTotPerSav += pricePerMinSaved
                                    nEastCarCount += 1

                                elif stat in yorkMost:
                                    yorkTotPerSav += pricePerMinSaved
                                    yorkCarCount += 1
                                
                                elif stat in nWestMost:
                                    nWestTotPerSav += pricePerMinSaved
                                    nWestCarCount += 1
                                
                                elif stat in eMidsMost:
                                    eMidTotPerSav += pricePerMinSaved
                                    eMidCarCount += 1
                                
                                elif stat in wMidsMost:
                                    wMidTotPerSav += pricePerMinSaved
                                    wMidCarCount += 1
                                
                                elif stat in walesMost:
                                    walesTotPerSav += pricePerMinSaved
                                    walesCarCount += 1
                                
                                elif stat in eastMost:
                                    eastTotPerSav += pricePerMinSaved
                                    eastCarCount += 1
                                
                                elif stat in sEastMost:
                                    sEastTotPerSav += pricePerMinSaved
                                    sEastCarCount += 1
                                
                                elif stat in sWestMost:
                                    sWestTotPerSav += pricePerMinSaved
                                    sWestCarCount += 1

                        # Price per metrics other than minutes saved
                        if outMileage != 0:
                            # Price per mile of track
                            pricePerMile = fare/outMileage

                            # Price per crow flies mile
                            pricePerCrowFliesMile = fare/crowFliesDist

                            # Price per minute of train journey
                            pricePerMinTrain = fare/trainTime

                            # Check which region journey is from
                            if stat in londonMost:
                                lonTotPerMile += pricePerMile
                                lonTotPerCrow += pricePerCrowFliesMile
                                lonTotPerMin += pricePerMinTrain
                                lonCount += 1

                            elif stat in scotMost:
                                scotTotPerMile += pricePerMile
                                scotTotPerCrow += pricePerCrowFliesMile
                                scotTotPerMin += pricePerMinTrain
                                scotCount += 1
                            
                            elif stat in nEastMost:
                                nEastTotPerMile += pricePerMile
                                nEastTotPerCrow += pricePerCrowFliesMile
                                nEastTotPerMin += pricePerMinTrain
                                nEastCount += 1

                            elif stat in yorkMost:
                                yorkTotPerMile += pricePerMile
                                yorkTotPerCrow += pricePerCrowFliesMile
                                yorkTotPerMin += pricePerMinTrain
                                yorkCount += 1
                            
                            elif stat in nWestMost:
                                nWestTotPerMile += pricePerMile
                                nWestTotPerCrow += pricePerCrowFliesMile
                                nWestTotPerMin += pricePerMinTrain
                                nWestCount += 1
                            
                            elif stat in eMidsMost:
                                eMidTotPerMile += pricePerMile
                                eMidTotPerCrow += pricePerCrowFliesMile
                                eMidTotPerMin += pricePerMinTrain
                                eMidCount += 1
                            
                            elif stat in wMidsMost:
                                wMidTotPerMile += pricePerMile
                                wMidTotPerCrow += pricePerCrowFliesMile
                                wMidTotPerMin += pricePerMinTrain
                                wMidCount += 1
                            
                            elif stat in walesMost:
                                walesTotPerMile += pricePerMile
                                walesTotPerCrow += pricePerCrowFliesMile
                                walesTotPerMin += pricePerMinTrain
                                walesCount += 1
                            
                            elif stat in eastMost:
                                eastTotPerMile += pricePerMile
                                eastTotPerCrow += pricePerCrowFliesMile
                                eastTotPerMin += pricePerMinTrain
                                eastCount += 1
                            
                            elif stat in sEastMost:
                                sEastTotPerMile += pricePerMile
                                sEastTotPerCrow += pricePerCrowFliesMile
                                sEastTotPerMin += pricePerMinTrain
                                sEastCount += 1
                            
                            elif stat in sWestMost:
                                sWestTotPerMile += pricePerMile
                                sWestTotPerCrow += pricePerCrowFliesMile
                                sWestTotPerMin += pricePerMinTrain
                                sWestCount += 1

            # Average price per mile of track for each region
            avTrackLon = lonTotPerMile/lonCount
            avTrackScot = scotTotPerMile/scotCount
            avTrackNEast = nEastTotPerMile/nEastCount
            avTrackYork = yorkTotPerMile/yorkCount
            avTrackNWest = nWestTotPerMile/nWestCount
            avTrackEMids = eMidTotPerMile/eMidCount
            avTrackWMids = wMidTotPerMile/wMidCount
            avTrackWales = walesTotPerMile/walesCount
            avTrackEast = eastTotPerMile/eastCount
            avTrackSEast = sEastTotPerMile/sEastCount
            avTrackSWest = sWestTotPerMile/sWestCount

            # Average price per mile as crow flies for each region
            avCrowLon = lonTotPerCrow/lonCount
            avCrowScot = scotTotPerCrow/scotCount
            avCrowNEast = nEastTotPerCrow/nEastCount
            avCrowYork = yorkTotPerCrow/yorkCount
            avCrowNWest = nWestTotPerCrow/nWestCount
            avCrowEMids = eMidTotPerCrow/eMidCount
            avCrowWMids = wMidTotPerCrow/wMidCount
            avCrowWales = walesTotPerCrow/walesCount
            avCrowEast = eastTotPerCrow/eastCount
            avCrowSEast = sEastTotPerCrow/sEastCount
            avCrowSWest = sWestTotPerCrow/sWestCount

            # Average price per min of journey
            avMinLon = lonTotPerMin/lonCount
            avMinScot = scotTotPerMin/scotCount
            avMinNEast = nEastTotPerMin/nEastCount
            avMinYork = yorkTotPerMin/yorkCount
            avMinNWest = nWestTotPerMin/nWestCount
            avMinEMids = eMidTotPerMin/eMidCount
            avMinWMids = wMidTotPerMin/wMidCount
            avMinWales = walesTotPerMin/walesCount
            avMinEast = eastTotPerMin/eastCount
            avMinSEast = sEastTotPerMin/sEastCount
            avMinSWest = sWestTotPerMin/sWestCount

            # Average price per minute saved
            avSavLon = lonTotPerSav/lonCarCount
            avSavScot = scotTotPerSav/scotCarCount
            avSavNEast = nEastTotPerSav/nEastCarCount
            avSavYork = yorkTotPerSav/yorkCarCount
            avSavNWest = nWestTotPerSav/nWestCarCount
            avSavEMids = eMidTotPerSav/eMidCarCount
            avSavWMids = wMidTotPerSav/wMidCarCount
            avSavWales = walesTotPerSav/walesCarCount
            avSavEast = eastTotPerSav/eastCarCount
            avSavSEast = sEastTotPerSav/sEastCarCount
            avSavSWest = sWestTotPerSav/sWestCarCount
            
            # Return information
            print("****")
            print("Average price per mile of track for London:", "£{:.2f}".format(avTrackLon), "Average price per mile as the crow flies for London:", "£{:.2f}".format(avCrowLon), "Average price per minute of train journey for London:", "£{:.2f}".format(avMinLon), "Average price per minute saved by using the train in London:", "£{:.2f}".format(avSavLon))
            print("")
            print("Average price per mile of track for Scotland:", "£{:.2f}".format(avTrackScot), "Average price per mile as the crow flies for Scotland:", "£{:.2f}".format(avCrowScot), "Average price per minute of train journey for Scotland:", "£{:.2f}".format(avMinScot), "Average price per minute saved by using the train in Scotland:", "£{:.2f}".format(avSavScot))
            print("")
            print("Average price per mile of track for North East:", "£{:.2f}".format(avTrackNEast), "Average price per mile as the crow flies for North East:", "£{:.2f}".format(avCrowNEast), "Average price per minute of train journey for North East:", "£{:.2f}".format(avMinNEast), "Average price per minute saved by using the train in North East:", "£{:.2f}".format(avSavNEast))
            print("")
            print("Average price per mile of track for Yorkshire and Humber:", "£{:.2f}".format(avTrackYork), "Average price per mile as the crow flies for Yorkshire and Humber:", "£{:.2f}".format(avCrowYork), "Average price per minute of train journey for Yorkshire and Humber:", "£{:.2f}".format(avMinYork), "Average price per minute saved by using the train in Yorkshire and Humber:", "£{:.2f}".format(avSavYork))
            print("")
            print("Average price per mile of track for North West:", "£{:.2f}".format(avTrackNWest), "Average price per mile as the crow flies for North West:", "£{:.2f}".format(avCrowNWest), "Average price per minute of train journey for North West:", "£{:.2f}".format(avMinNWest), "Average price per minute saved by using the train in North West:", "£{:.2f}".format(avSavNWest))
            print("")
            print("Average price per mile of track for East Midlands:", "£{:.2f}".format(avTrackEMids), "Average price per mile as the crow flies for East Midlands:", "£{:.2f}".format(avCrowEMids), "Average price per minute of train journey for East Midlands:", "£{:.2f}".format(avMinEMids), "Average price per minute saved by using the train in East Midlands:", "£{:.2f}".format(avSavEMids))
            print("")
            print("Average price per mile of track for West Midlands:", "£{:.2f}".format(avTrackWMids), "Average price per mile as the crow flies for West Midlands:", "£{:.2f}".format(avCrowWMids), "Average price per minute of train journey for West Midlands:", "£{:.2f}".format(avMinWMids), "Average price per minute saved by using the train in West Midlands:", "£{:.2f}".format(avSavWMids))
            print("")
            print("Average price per mile of track for Wales:", "£{:.2f}".format(avTrackWales), "Average price per mile as the crow flies for Wales:", "£{:.2f}".format(avCrowWales), "Average price per minute of train journey for Wales:", "£{:.2f}".format(avMinWales), "Average price per minute saved by using the train in Wales:", "£{:.2f}".format(avSavWales))
            print("")
            print("Average price per mile of track for East of England:", "£{:.2f}".format(avTrackEast), "Average price per mile as the crow flies for East of England:", "£{:.2f}".format(avCrowEast), "Average price per minute of train journey for East of England:", "£{:.2f}".format(avMinEast), "Average price per minute saved by using the train in East of England:", "£{:.2f}".format(avSavEast))
            print("")
            print("Average price per mile of track for South East:", "£{:.2f}".format(avTrackSEast), "Average price per mile as the crow flies for South East:", "£{:.2f}".format(avCrowSEast), "Average price per minute of train journey for South East:", "£{:.2f}".format(avMinSEast), "Average price per minute saved by using the train in South East:", "£{:.2f}".format(avSavSEast))
            print("")
            print("Average price per mile of track for South West:", "£{:.2f}".format(avTrackSWest), "Average price per mile as the crow flies for South West:", "£{:.2f}".format(avCrowSWest), "Average price per minute of train journey for South West:", "£{:.2f}".format(avMinSWest), "Average price per minute saved by using the train in South West:", "£{:.2f}".format(avSavSWest))
            print("")

            # Plot averages on bar chart
            n = 4
            ind = np.arange(n)
            wid = 0.05
            plt.rcParams["figure.figsize"] = (15,10)

            ldn = [avTrackLon, avCrowLon, avMinLon, avSavLon]
            bar1 = plt.bar(ind, ldn, wid, color = 'r')

            scot = [avTrackScot, avCrowScot, avMinScot, avSavScot]
            bar2 = plt.bar(ind+wid, scot, wid, color = 'g')

            nEast = [avTrackNEast, avCrowNEast, avMinNEast, avSavNEast]
            bar3 = plt.bar(ind+wid*2, nEast, wid, color = 'b')

            yorkHumb = [avTrackYork, avCrowYork, avMinYork, avSavYork]
            bar4 = plt.bar(ind+wid*3, yorkHumb, wid, color = 'c')

            nWest = [avTrackNWest, avCrowNWest, avMinNWest, avSavNWest]
            bar5 = plt.bar(ind+wid*4, nWest, wid, color = 'm')

            eMids = [avTrackEMids, avCrowEMids, avMinEMids, avSavEMids]
            bar6 = plt.bar(ind+wid*5, eMids, wid, color = 'y')

            wMids = [avTrackWMids, avCrowWMids, avMinWMids, avSavWMids]
            bar7 = plt.bar(ind+wid*6, wMids, wid, color = 'k')

            wales = [avTrackWales, avCrowWales, avMinWales, avSavWales]
            bar8 = plt.bar(ind+wid*7, wales, wid, color = '#A200FF')

            east = [avTrackEast, avCrowEast, avMinEast, avSavEast]
            bar9 = plt.bar(ind+wid*8, east, wid, color = '#7A7A7A')

            sEast = [avTrackSEast, avCrowSEast, avMinSEast, avSavSEast]
            bar10 = plt.bar(ind+wid*9, sEast, wid, color = '#FE8300')

            sWest = [avTrackSWest, avCrowSWest, avMinSWest, avSavSWest]
            bar11 = plt.bar(ind+wid*10, sWest, wid, color = '#00E487')

            plt.xlabel("Metrics")
            plt.ylabel('Average Fare in Pounds')
            plt.title("Average Fares")

            plt.xticks(ind+wid,['Per Mile of Track', 'Per Crow Flies Mile', 'Per Minute', 'Per Minute Saved'])
            plt.legend( (bar1, bar2, bar3, bar4, bar5, bar6, bar7, bar8, bar9, bar10, bar11), ('London', 'Scotland', 'North East', 'Yorkshire & The Humber', 'North West', 'East Midlands', 'West Midlands', 'Wales', 'East of England', 'South East', 'South West') )
            plt.show()
        
        # Quit
        elif functionSelect == 0:
            print("You have quit the program.")
            exit()
        
        # For anything else
        else:
            print("Your entry is not valid.")
    
    except ValueError:
        print("You did not enter a number.")
        