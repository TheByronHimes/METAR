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

def sToI(s):
    try:
        return int(s)
    except ValueError:
        print("Error: Could not convert value to integer")
        exit(0)

def isReportType(fText, key, d):
    # Returns bool indicating whether the field is "Type of Report"
    # Values: "METAR" or "SPECI"
    if fText.upper() == ("METAR" or "SPECI"):
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
    date = sToI(fText[0:2])
    hour = sToI(fText[2:4])
    minute = sToI(fText[4:6])

    # Ensure values fall within expected range
    if fText.upper()[-1] == "Z":
        if 0 <= date <= 31:
            if 0 <= hour <= 23:
                if 0 <= minute <= 59:
                    d[key] = "Date and Time of Report: "
                    return True
    else:
        return False

def isReportModifier(fText, key, d):
    # Returns bool indicating whether the field is "Report Modifier"
    # Values: "AUTO" or "COR"
    if fText == ("AUTO" or "COR"):
        d[key] = "Report Modifier: "
        return True
    else:
        return False

def isWindGroup1(fText, key, d):
    # Returns bool indicating whether the field is "Wind Group"
    # Format: dddff(f)GmmmKT
    # ddd = wind direction (000 - 369) OR "VRB"
    # ff(f) = wind speed (00-999)
    # G = string literal indicating "Gust"
    # mmm = wind gust speed (000 - 999)
    # KT = string literal indicating "knots"

    
    # determine if ddd is VRB or 3-digit integer
    if fText[0:3] == "VRB":
        ddd = fText[0:3]
    else:
        ddd = sToI(fText[0:3])
        
    # Validate field text length as 11 or 12 chars
    if len(fText) == 11:
        ff = sToI(fText[3:5])
        mmm = sToI(fText[6:9])
        G = fText[5].upper()
        KT = fText[9:].upper()
        if 0 <= ff <= 99 and G == "G" and KT == "KT":
                if 0 <= mmm <= 999:
                        d[key] = "Wind: "
                        return True
    elif len(fText) == 12:
        fff = sToI(fText[3:6])
        mmm = sToI(fText[7:10])
        G = fText[6].upper()
        KT = fText[10:].upper()
        if (0 <= (fff and mmm) <= 999) and (G == "G") and (KT == "KT"):
                        d[key] = "Wind: "
                        return True
    else:
        return False

def isWindGroup2(fText, key, d):
    # Returns bool indicating whether the field is variable high speed wind info
    # This will be appended to WindGroup1 information with a space in between if
    #     present
    # Format: nnnVxxx
    # nnn = lower end of variability range (000 - 359)
    # V = string literal indicating "variable" (haha)
    # xxx = upper end of variability range (000 - 359)

    # Validate length as 7 chars
    if len(fText) == 7:
        nnn = sToI(fText[0:3])
        xxx = sToI(fText[4:])
        if (fText[3].upper() == "V"):
            if 0 <= (nnn and xxx) <= 359:
                d[key] = "WIND2"
                return True            
    else:
        return False
        
    

# Program entry:
if __name__ == "__main__":

    # get raw metar reading
    metar_reading = getReading()

    # populate the fields dictionary
    for i in (0, len(metar_reading)):
        fields[i] = ""
