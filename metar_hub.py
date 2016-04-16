'''
AUTHOR: Byron Himes
MODIFIED: 11 April 2016
DESCRIPTION: Takes a METAR reading as input and outputs the interpretation (meaning).
FILES: metar_hub.py, interpreter.py, metar.py, metar_scrape.py
'''

import sys
import interpreter
from metar import Metar
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
    report = Metar(metar_scrape.getReport(targetStation))

    components = [
    interpreter.stationID(report.getStationID()),
    interpreter.dateTime(report.getDateTime()),
    interpreter.reportModifier(report.getModifier()),
    interpreter.windGroup(report.getWind()),
    interpreter.visibilityGroup(report.getVisibility()),
    interpreter.runwayVisibilityRange(report.getRunway()),
    interpreter.skyCondition(report.getSky()),
    interpreter.tempDewPoint(report.getTempDewPoint()),
    interpreter.altimeter(report.getAltimeter())
    ]

    print("\n------------------------------------------------------")
    for component in components:
        if component != None and len(component) > 1:
            print(component)
            print('')
    print("------------------------------------------------------")
