'''
AUTHOR: Byron Himes
MODIFIED: 28 March 2016
DESCRIPTION: Takes a METAR reading as input and outputs the interpretation (meaning).
FILES: metar.py
'''

# define a dictionary to label the fields dynamically
fields = {}

def getReading():
    # this function prompts the user to enter the data
    # will modify later to provide options for file input or CL input
    reading = input("Enter METAR reading: ")
    return reading

def isReportType(fText, key, d):
    # Returns bool indicating whether the field is "Type of Report"
    # Values: "METAR" or "SPECI"
    if fText.upper() == "METAR" or fText.upper() == "SPECI":
        d[key] = "Type of Report: "
        return True
    else:
        return False


def isStationID(fText, key, d):
    # Returns bool indicating whether the field is "Station ID"
    # Format: AAAA (four alpha chars)
    for char in fText:
        if char.isalpha == False:
            return False
    else:
        d[key] = "Station ID: "
        return True

def isDateTime(fText, key, d):
    # Returns bool indicating whether the field is "Date and Time of Report"
    # Format: DDTTttZ
    # DD = day of the month (01 - 31)
    # TT = hour of the report (00 - 23)
    # tt = minute of the report (00 - 59)
    # Z is a string literal which indicates Zulu time.

    # Validate field text length
    if len(fText) > 7 or len(fText) < :
        return False

    for i in fText[0:6]:
        if i.isalpha() != True:
            return False

    # Cast expected date & time values to ints
    date = int(fText[0:2])
    hour = int(fText[2:4])
    minute = int(fText[4:6])

    # Ensure values fall within expected range
    if fText.upper()[-1] == "Z":
        if date >= 0 and date <= 31:
            if hour >= 0 and hour <= 23:
                if minute >= 0 and minute <= 59:
                    d[key] = "Date and Time of Report: "
                    return True
    else:
        return False

def isReportModifier(fText, key, d):
    # Returns bool indicating whether the field is "Report Modifier"
    # Values: "AUTO" or "COR"
    if fText == "AUTO" or fText == "COR":
        d[key] = "Report Modifier: "
        return True
    else:
        return False

def isWindGroup1(fText, key, d):
    # Returns bool indicating whether the field is "Wind: "
    # Format: dddff(f)GmmmKT
    # ddd = wind direction (000 - 369) OR "VRB"
    # ff(f) = wind speed (01-999)
    # G = string literal indicating "Gust"
    # mmm = wind gust speed (000 - 999)
    # KT = string literal indicating "knots"

def isWindGroup2(fText, key, d):
    # Returns bool indicating whether the field is variable high speed wind info
    # This will be appended to WindGroup1 information with a space in between if
    #     present
    # Format: nnnVxxx
    # nnn = lower end of variability range (000 - 359)
    # V = string literal indicating "variable" (haha)
    # xxx = upper end of variability range (000 - 359)
    

# Program entry:
if __name__ == "__main__":

    # get raw metar reading
    metar_reading = getReading()

    # populate the fields dictionary
    for i in (0, len(metar_reading)):
        fields[i] = ""
