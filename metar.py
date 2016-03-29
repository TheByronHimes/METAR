'''
AUTHOR: Byron Himes
MODIFIED: 29 March 2016
DESCRIPTION: Takes a METAR reading as input and outputs the interpretation (meaning).
FILES: metar.py
'''

import re

# define a dictionary to label the fields dynamically
fields = {}

def getReading():
    # this function prompts the user to enter the data
    # will modify later to provide options for file input or CL input
    reading = input("Enter METAR reading: ")
    return reading

def sToI(s):
    try:
        return int(s)
    except ValueError:
        print("Error: Could not convert value to integer")
        exit(0)

def stationID(fText, key, d):
    # Returns bool indicating whether the field is "Station ID"
    # Format: AAAA (four alpha chars)
    idPattern = re.compile('[A-Z]{4}\s')
    match = re.match(idPattern, fText)
    if match != None:
        d[key] = fText[match.start():match.end()]
        return True
    else:
        return False

def dateTime(fText, key, d):
    # Returns bool indicating whether the field is "Date and Time of Report"
    # Format: DDTTttZ
    # DD = day of the month (01 - 31)
    # TT = hour of the report (00 - 23)
    # tt = minute of the report (00 - 59)
    # Z is a string literal which indicates Zulu time.
    dtPattern = re.compile('([0-3][0-9])([0-2][0-9][0-5][0-9])Z')
    match = re.match(dtPattern, fText)
    if match != None:
        d[key] = None
        return True
    else:
        return False

def reportModifier(fText, key, d):
    # Returns bool indicating whether the field is "Report Modifier"
    # Values: "AUTO" or "COR"
    if fText == ("AUTO" or "COR"):
        d[key] = "Report Modifier: "
        return True
    else:
        return False

def windGroup(fText, key, d):
    # Returns bool indicating whether the field is "Wind Group"
    # Format: dddff(f)GmmmKT_nnnVxxx
    # ddd = wind direction (000 - 369) OR "VRB"
    # ff(f) = wind speed (00-999)
    # G = string literal indicating "Gust"
    # mmm = wind gust speed (000 - 999)
    # KT = string literal indicating "knots"
    # _ = space
    # nnn = lower end of variability range (000 - 359)
    # V = string literal indicating "variable" (haha)
    # xxx = upper end of variability range (000 - 359)

    # try to match the entire field set first
    windPattern = re.compile('((VRB|[0-3][0-9]{1,2})([0-9]{2,3})(G[0-9]{2,3})?KT|00000KT)(\s[0-3][0-9]{1,2}V[0-3][0-9]{1,2})?')
    match = re.match(windPattern, fText)

    # if found, break it down into its subgroups for easy printing later
    # store list of subgroups in format ordered as listed above
    if match != None:
        d[key] = "Wind Group: "
        return True
    else:
        return False
        
    

# Program entry:
if __name__ == "__main__":

    # get raw metar reading
    metar = getReading()

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
