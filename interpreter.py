'''
AUTHOR: Byron Himes
MODIFIED: 11 April 2016
DESCRIPTION: A set of functions to interpret METAR report fields.
FILES: metar_interpreter.py
'''

import re

def degreesToDirection(i):
    # This function takes an integer, i, and converts it to the corresponding
    # compass direction, d, where 0 degrees is N for North
    if type(i) == str:
        i = int(i)
    
    if 0 <= i < 11 or 349 <= i < 360:
        d = "N"
    elif 11 <= i < 34:
        d = "NNE"
    elif 34 <= i < 56:
        d = "NE"
    elif 56 <= i < 79:
        d = "ENE"
    elif 79 <= i < 101:
        d = "E"
    elif 101 <= i < 124:
        d = "ESE"
    elif 124 <= i < 146:
        d = "SE"
    elif 146 <= i < 169:
        d = "SSE"
    elif 169 <= i < 191:
        d = "S"
    elif 191 <= i < 214:
        d = "SSW"
    elif 214 <= i < 236:
        d = "SW"
    elif 236 <= i < 259:
        d = "WSW"
    elif 259 <= i < 281:
        d = "W"
    elif 281 <= i < 304:
        d = "WNW"
    elif 304 <= i < 326:
        d = "NW"
    elif 326 <= i < 349:
        d = "NNW"
    return d

def stationID(text):
    # Translates station ID from raw to readable
    toPrint = "Station ID: " + text.upper()
    return toPrint

def dateTime(text):
    # Translates date and time from raw to readable
    # Format: DDTTttZ
    # DD = day of the month (01 - 31)
    # TT = hour of the report (00 - 23)
    # tt = minute of the report (00 - 59)
    # Z is a string literal which indicates Zulu time.
    toPrint = ""
    day = text[0:2] # this is not a secure way of getting the info
    hour = text[2:4]
    minute = text[4:6]
    toPrint += "Day of Month: " + day
    toPrint += "\nTime: " + hour + ":" + minute
    return toPrint

def reportModifier(text):
    # Translates report modifier from raw to readable
    # Values: "AUTO" or "COR"
    toPrint = "Report Modifier: " + text.upper()
    

def windGroup(fText, key, d):
    # Translates wind group information from raw to readable
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

    # go left to right, stripping off the information as we get it
    toPrint = ""

    # retrieve and strip direction info (ddd)
    dirPattern = re.compile('(VRB|[0-3]\d{1,2})')
    dirMatch = re.search(dirPattern, text)
    if dirMatch != None:
        ddd = dirMatch.group()

        # if ddd is VRB, change it to read "Variable" for the user's ease
        if ddd == "VRB":
            ddd = "Variable"
        toPrint += "\nDirection: " + degreesToDirection(int(ddd))
        text = text[dirMatch.end():]

    # retrieve and strip wind speed info (ff(f))
    speedPattern = re.compile('(\d{2,3})')
    speedMatch = re.match(speedPattern, text) # use match, going L to R
    if speedMatch != None:
        fff = int(speedMatch.group())
        fff *= 1.15 #convert from km to mi
        if fff == 0:
            toPrint += "\nSpeed: Calm (none to very light)"
        else:
            toPrint += "\nSpeed: " + "%.f" % fff + "mph"
        text = text[speedMatch.end():]

    # retrieve and strip wind gust info (Gmmm)           
    gustPattern = re.compile('(G\d{2,3})')
    gustMatch = re.search(gustPattern, text)
    if gustMatch != None:
        # the G is a literal, so we're only interested in the speed (mmm)
        mmm = int(gustMatch.group()[1:])
        mmm *= 1.15 #convert from km to mi
        toPrint += "\nWind gusts of up to " + "%.f" % mmm + "mph"
        text = text[gustMatch.end():]

    # strip 'KT' if it is there (it should be there in a valid wind field)
    kt_loc = text.find("KT")
    if kt_loc > -1:
        text = text[kt_loc + 2:]

    # retrieve and strip variable wind range info (nnnVxxx)
    vrbPattern = re.compile('([0-3]\d{1,2}V[0-3]\d{1,2})')
    vrbMatch = re.search(vrbPattern, text)
    if vrbMatch != None:
        vrb = vrbMatch.group()
        angle1 = vrb[:vrb.find('V')] + " degrees "
        angle2 = vrb[vrb.find('V')+1:] + " degrees "
        toPrint += "\nDirection varying from " + angle1 + "to " + angle2
    return toPrint

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
        'M?(([1-9]\s[1-9]/[1-9])|([1-9]/[1-9])|(\d{1,2}))SM'
    )
    visMatch = re.search(visPattern, fText)
    if visMatch != None:
        toPrint = ""
        mText = visMatch.group()
        mText = mText[:mText.find("SM")]
        m_loc = mText.find("M")
        if m_loc > -1:
            toPrint += "Less than " + mText[m_loc+1:] + " statute miles"
        elif m_loc == -1:
            toPrint += "\n\t" + mText + " statute miles"
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
    rvPattern = re.compile('(R\d{2}[CRL]?/\d{4}FT)|(R\d{2}[CRL]?/\d{4}V\d{4}FT)')
    longPattern = re.compile('')

    #try to match long pattern first, then short pattern
    longMatch = re.search(longPattern, fText)
    shortMatch = re.search(shortPattern, fText)
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

def presentWeather(fText, key, d):
    # Looks for and culls present weather group information from metar string
    # Format: w'w'
    pass

def skyCondition(fText, key, d):
    # Looks for and culls sky condition information from metar string
    # Format: NNNhhh OR VVsss OR SKC|CLR
    # NNN = amount of sky cover (3 letters)
    # hhh = height of sky cover layer
    # VV = string literal indicating "indefinite ceiling"
    # sss = vertical visibility into indefinite ceiling
    # SKC = string literal used by manual stations = "clear skies"
    # CLR = string literal used by automated stations = "clear skies"
    # NOTE: may sky conditions groups may be present in the metar body

    skyPattern = re.compile('[A-Z]{3}\d{3}')
    vertPattern = re.compile('VV\d{3}')
    clearPattern = re.compile('SKC|CLR')
    skyMatches = re.findall(skyPattern, fText)
    vertMatches = re.findall(vertPattern, fText)
    clearMatches = re.findall(clearPattern, fText)
    
    if len(skyMatches) == 0 and len(vertMatches) == 0 and len(clearMatches) == 0:
        return False
    else:
        toString = ""
        for i in skyMatches:
            if i[:3] == "FEW":
                toString += "\n\tFew clouds at "
                toString += str(int(i[3:]) * 100) + "ft"
            elif i[:3] == "SCT":
                toString += "\n\tScattered clouds at "
                toString += str(int(i[3:]) * 100) + "ft"
            elif i[:3] == "BKN":
                toString += "\n\tBroken clouds at "
                toString += str(int(i[3:]) * 100) + "ft"
            elif i[:3] == "OVC":
                toString += "\n\tOvercast at "
                toString += str(int(i[3:]) * 100) + "ft"
        for i in vertMatches:
            toString += "\n\tIndefinite ceiling with visibility up to "
            toString += str(int(i[3:]) * 100) + "ft"
        for i in clearMatches:
            toString += "\n\tClear skies"
        d[key] = toString
        return True

def tempDewPoint(fText, key, d):
    # Looks for and culls temperature and dew point info from METAR (fText)
    # Format: TsT'T'T'sD'D'D'
    # NOTE: temps are reported in degrees celcius
    # T = string literal indicating "temperature"
    # s = sign of the temperature and dew point (1 for - or 0 for -)
    # T'T'T' = temperature (000-999)
    # D'D'D' = dew point temperature (000-999)
    tdPattern = re.compile('T[01]\d{3}[01]\d{3}')
    tdMatch = re.search(tdPattern, fText)
    if tdMatch != None:
        # if temp and dew point is reported, get the information
        toString = ""
        mText = tdMatch.group()

        # strip literal 'T'
        mText = mText[1:]

        # get temperature and its sign, then strip that info from mText
        if mText[0] == '1':
            temp_Celcius = -1 * float(mText[1:4])/10
            temp_Fahrenheit = temp_Celcius * (9/5) + 32
            toString += "\n\tTemperature: " + str(temp_Celcius) + "ºC, "
            toString += "%.f" % temp_Fahrenheit + "ºF"
        elif mText[0] == '0':
            temp_Celcius = float(mText[1:4])/10
            temp_Fahrenheit = temp_Celcius * (9/5) + 32
            toString += "\n\tTemperature: " + str(temp_Celcius) + "ºC, "
            toString += "%.f" % temp_Fahrenheit + "ºF"
        mText = mText[4:]

        # get dew point and its sign
        dp_Celcius = float(mText[1:])/10
        dp_Fahrenheit = dp_Celcius * (9/5) + 32.

        # for the sign, 1 = -, 0 = +
        if mText[0] == '1':
            dp_Celcius *= -1
            dp_Fahrenheit = dp_Celcius * (9/5) + 32
            toString += "\n\tDew Point: " + str(dp_Celcius) + "ºC, "
            toString += "%.f" % dp_Fahrenheit + "ºF"
        elif mText[0] == '0':
            toString += "\n\tDew Point: " + str(dp_Celcius) + "ºC, "
            toString += "%.f" % dp_Fahrenheit + "ºF"

        # store output in dictionary
        d[key] = toString
        return True
    else:
        return False

def altimeter(fText, key, d):
    # Looks for and culls altimeter data from metar string
    # Format: APPPP
    # A = string literal indicating "Altimeter in inches of mercury"
    # PPPP = four digit group representing PP.PPin hg (decimal excluded)
    altPattern = re.compile('A\d{4}')
    altMatch = re.search(altPattern, fText)
    print("got this far")

    if altMatch != None:
        toString = ""
        mText = altMatch.group()
        reading = float(mText[1:])/100
        toString = "\n\tAltimeter: %.2f" % reading + "in"

        # store output
        d[key] = toString
        return True
    else:
        return False
        


        
        
