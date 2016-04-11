'''
AUTHOR: Byron Himes
MODIFIED: 11 April 2016
DESCRIPTION: Takes a METAR reading as input and outputs the interpretation (meaning).
FILES: metar_hub.py, interpreter.py, metar.py, metar_scrape.py
'''

import sys
import interpreter
import metar
import metar_scrape

# Program entry:
if __name__ == "__main__":
    try:
        targetStation = sys.argv[1]
    except IndexError:
        print("Input 4-letter station id as command line arg")
        print("Example usage: metar_hub.py ksgf")
        exit(0)

    # get metar report and put it into a Metar object
    report = metar.Metar(metar_scrape.getReport(targetStation))
    
    
    '''
    loopBool = "c"

    # choose station
    station = input("Enter station ID for report source: ")

    while loopBool == "c":
        
        # get raw metar reading
        metar = metarScrape.getReport(station)
        print(metar)

        # list of ordered dict keys
        keys = [
            "Station ID: ",
            "Date and Time of Report: ",
            "Report Modifier: ",
            "Wind: ",
            "Visibility: ",
            "Runway Visual Range: ",
            "Present Weather: ",
            "Sky Condition: ",
            "Temperature and Dew Point: ",
            "Altimeter: ",
            "Remarks: "
        ]

        fields = {}

        stationID(metar, keys[0], fields)
        dateTime(metar, keys[1], fields)
        reportModifier(metar, keys[2], fields)
        windGroup(metar, keys[3], fields)
        visibilityGroup(metar, keys[4], fields)
        runwayVisibilityRange(metar, keys[5], fields)
        # presentWeather(metar, keys[6], fields) not implemented yet
        skyCondition(metar, keys[7], fields)
        tempDewPoint(metar, keys[8], fields)
        altimeter(metar, keys[9], fields)

        print('\n---------------------------------------------------------\n')
        for k in keys:
            if k in fields.keys():
                print(k, fields[k])
                
        # ask user if they would like to refresh the data
        loopBool = input("Enter 'c' to continue or any other letter to stop: ")
        '''
