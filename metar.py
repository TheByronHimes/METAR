'''
AUTHOR: Byron Himes
MODIFIED: 30 March 2016
DESCRIPTION: Takes a METAR reading as input and outputs the interpretation (meaning).
FILES: metar.py
'''

import re

# define a dictionary to label the fields dynamically
fields = {}

def getReading():
    # this function prompts the user to enter the metar report string
    # will modify later to provide options for file input or CL input
    reading = input("Enter METAR reading: ").upper()

    # strip the METAR or SPECI report type info
    if ("METAR" | "SPECI") in reading:
        reading = reading[6:]
    return reading

def stationID(fText, key, d):
    # Looks for and culls station id information from metar string
    # Format: AAAA (four alpha chars)
    idPattern = re.compile('[A-Z]{4}\s')
    match = re.match(idPattern, fText)
    if match != None:
        d[key] = fText[match.start():match.end()]
        return True
    else:
        return False

def dateTime(fText, key, d):
    # Looks for and culls date & time information from metar string
    # Format: DDTTttZ
    # DD = day of the month (01 - 31)
    # TT = hour of the report (00 - 23)
    # tt = minute of the report (00 - 59)
    # Z is a string literal which indicates Zulu time.
    dtPattern = re.compile('([0-3][0-9])([0-2][0-9][0-5][0-9])Z')
    match = re.match(dtPattern, fText)
    
    if match != None:
        toPrint = ""
        mText = match.group()
        day = mText[0:2]
        hour = mText[2:4]
        minute = mText[4:6]
        toPrint += "\n\tDay of Month: " + day
        toPrint += "\n\tTime: " + hour + ":" + minute
        d[key] = toPrint
        return True
    else:
        return False

def reportModifier(fText, key, d):
    # Looks for and culls report modifier information from metar string
    # Values: "AUTO" or "COR"
    modPattern = re.compile('(AUTO|COR)')
    match = re.match(modPattern, fText)
    if match != None:
        d[key] = match.group()
        return True
    else:
        return False

def windGroup(fText, key, d):
    # Looks for and culls wind group information from metar string
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
    windPattern = re.compile(
        '((VRB|[0-3][0-9]{1,2})([0-9]{2,3})(G[0-9]{2,3})?KT|00000KT)(\s[0-3][0-9]{1,2}V[0-3][0-9]{1,2})?'
    )
    match = re.match(windPattern, fText)

    # if found, break it down into its subgroups for easy printing later
    # go left to right, stripping off the information as we get it
    if match != None:
        toPrint = ""
        mText = match.group()

        # retrieve and strip direction info (ddd)
        dirPattern = re.compile('(VRB|[0-3][0-9]{1,2})')
        dirMatch = re.match(dirPattern, mText)
        if dirMatch != None:
            ddd = dirMatch.group()

            # if ddd is VRB, change it to read "Variable" for the user's ease
            if ddd == "VRB":
                ddd = "Variable"
            toPrint += "\n\tDirection: " + ddd + " degrees"
            mText = mText[dirMatch.end()+1:]

        # retrieve and strip wind speed info (ff(f))
        speedPattern = re.compile('([0-9]{2,3})')
        speedMatch = re.match(speedPattern, mText)
        if speedMatch != None:
            fff = int(speedMatch.group())
            if fff == 0:
                toPrint += "\n\tSpeed: Calm (none to very light)"
            else:
                toPrint += "\n\tSpeed: " + str(1.15*fff) + "mph"
            mText = mText[speedMatch.end()+1:]

        # retrieve and strip wind gust info (Gmmm)           
        gustPattern = re.compile('(G[0-9]{2,3})')
        gustMatch = re.match(gustPattern, mText)
        if gustMatch != None:
            # the G is a literal, so we're only interested in the speed (mmm)
            mmm = int(gustMatch.group()[1:])
            toPrint += "\n\tWind gusts of up to " + str(1.15*mmm) + "mph"
            mText = mText[gustMatch.end()+1:]

        # strip 'KT' if it is there (it should be there in a valid wind field)
        kt_loc = mText.find("KT")
        if kt_loc > -1:
            mText = mText[kt_loc + 2:]

        # retrieve and strip variable wind range info (nnnVxxx)
        vrbPattern = re.compile('([0-3][0-9]{1,2}V[0-3][0-9]{1,2})')
        vrbMatch = re.match(vrbPattern, mText)
        if vrbMatch != None:
            vrb = vrbMatch.group()
            angle1 = vrb[:vrb.find('V')] + " degrees "
            angle2 = vrb[vrb.find('V')+1:] + " degrees "
            toPrint += "\n\tDirection varying from " + angle1 + "to " + angle2
        d[key] = toPrint
        return True
    else:
        return False

def visibilityGroup(fText, key, d):
    # Looks for and culls visibility group information from metar string
    # Format: VVVVVSM
    # VVVVV = whole numbers, fractions, or mixed fractions.
    #     example values:
    #     M 1/4 where M signifies "less than"
    #     4 3/4
    #     1/4
    # SM = literal meaning "Statute Miles"
    visPattern = re.compile(
        'M?(([1-9]\s[1-9]/[1-9])|([1-9]/[1-9])|([0-9]{1,2}))SM'
    )
    visMatch = re.match(visPatter, fText)
    if visMatch != None:
        toPrint = ""
        mText = visMatch.group()
        mText = mText[:mText.find("SM")]
        m_loc = mText.find("M")
        if m_loc > -1:
            toPrint += "Less than " + mText[m_loc+1:] + " statute miles"
        elif m_loc == -1:
            toPrint += mText + "statute miles"
        d[key] = toPrint
        return True
    else:
        return False

def runwayVisibilityRange(fText, key, d):
    # Looks for and culls the runway visibility information from metar string
    # 2 Formats: RDD(D)/VVVVFT or RDD(D)/nnnnVxxxxFT
    # R = string literal indicating that the runway number follows next
    # DD = integer indicating the runway number (00-99)
    # D = [R | L | C] indicating runway approach direction.
    # / = string literal to separate runway no. and constant reportable value
    # VVVV = constant reportable value
    # FT = string literal indicating "feet"
    # nnnn = lowest reportable value in feet
    # V = string literal separating lowest and highest values
    # xxxx = highest reportable value in feet
    shortPattern = re.compile('(R[0-9]{2}[CRL]?/[0-9]{4}FT)')
    longPattern = re.compile('(R[0-9]{2}[CLR]?/[0-9]{4}V[0-9]{4}FT)')

    #try to match long pattern first, then short pattern
    longMatch = re.match(longPattern, fText)
    shortMatch = re.match(shortPattern, fText)
    if longMatch == None and shortMatch == None:
        return False
    elif shortMatch != None:
        # get short pattern data
        toString = ""
        mText = shortMatch.group()

        # strip the 'R' from the front of the string
        mText = mText[1:]

        # retrieve and strip DD(D) info
        DD = mText[:mText.find("/")]
        mText = mText[mText.find("/")+1:]
        toString += "\n\tRunway Number: " + DD
        
        # retrieve constant reportable value
        VVVV = mText[:mText.find("FT")]
        toString += "\n\tVisibility constant at: " + VVVV

        # store output string in dictionary
        d[key] = toString
        return True
    
    elif longMatch != None:
        # get long pattern data
        toString = ""
        mText = longMatch.group()

        # strip the 'R' from the front of the string
        mText = mText[1:]

        # retrieve and strip runway number info, DD(D)
        DD = mText[:mText.find("/")]
        mText = mText[mText.find("/")+1:]
        toString += "\n\tRunway Number: " + DD

        # retrieve and strip lowest reportable value, nnnn
        nnnn = mText[:mText.find("V")]
        mText = mText[mText.find("V")+1:]

        # retrieve highest reportable value, xxxx
        xxxx = mText[:mText.find("FT")]
        toString = "\n\tVisibility varying from " + nnnn + "ft - " + xxxx + "ft"

        # store output string in dictionary
        d[key] = toString
        return True    

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
    

    for k in keys:
        if k in fields.keys():
            print(k, fields[k])

