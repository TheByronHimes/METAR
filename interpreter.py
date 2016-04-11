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
    

def windGroup(text):
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

def visibilityGroup(text):
    # Translates visibility group info from raw to readable
    # Format: VVVVVSM
    # VVVVV = whole numbers, fractions, or mixed fractions.
    #     example values:
    #     M 1/4 where M signifies "less than"
    #     4 3/4
    #     1/4
    # SM = literal meaning "Statute Miles"
    toPrint = "Visibility: "
    text = text[:mText.find("SM")]
    m_loc = text.find("M")
    if m_loc > -1:
        toPrint += "Less than " + text[m_loc+1:] + " statute miles"
    elif m_loc == -1:
        toPrint += "\n" + text + " statute miles"
    return toPrint

def runwayVisibilityRange(text):
    # Translates runway visibility group from raw to readable
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

    # simple diff between formats is presence of literal 'V'
    toPrint = ""
    
    if "V" not in text:
        # get short pattern data
        # strip the 'R' from the front of the string
        text = text[1:]

        # retrieve and strip DD(D) info
        DD = text[:text.find("/")]
        text = text[text.find("/")+1:]
        toPrint += "\nRunway Number: " + DD
        
        # retrieve constant reportable value
        VVVV = text[:text.find("FT")]
        toPrint += "\nVisibility constant at: " + VVVV
    
    elif "V" in text:
        # get long pattern data
        # strip the 'R' from the front of the string
        text = text[1:]

        # retrieve and strip runway number info, DD(D)
        DD = text[:text.find("/")]
        text = text[text.find("/")+1:]
        toPrint += "\nRunway Number: " + DD

        # retrieve and strip lowest reportable value, nnnn
        nnnn = text[:text.find("V")]
        text = text[text.find("V")+1:]

        # retrieve highest reportable value, xxxx
        xxxx = text[:text.find("FT")]
        toPrint = "\nVisibility varying from " + nnnn + "ft - " + xxxx + "ft"
    return toPrint

def presentWeather(weathers):
    # NOTE: expects weathers as a List
    # Translates present weather group info from raw to readable
    # Format: w'w'
    pass

def skyCondition(conditions):
    # NOTE: expects conditions as a List
    # Translates sky condition group info from raw to readable
    # Format: NNNhhh OR VVsss OR SKC|CLR
    # NNN = amount of sky cover (3 letters)
    # hhh = height of sky cover layer
    # VV = string literal indicating "indefinite ceiling"
    # sss = vertical visibility into indefinite ceiling
    # SKC = string literal used by manual stations = "clear skies"
    # CLR = string literal used by automated stations = "clear skies"
    # NOTE: may sky conditions groups may be present in the metar body
    
    toPrint = ""
    for condition in conditions:
        if condition[:3] == "FEW":
            toPrint += "\nFew clouds at "
            toPrint += str(int(condition[3:]) * 100) + "ft"
        elif condition[:3] == "SCT":
            toPrint += "\nScattered clouds at "
            toPrint += str(int(condition[3:]) * 100) + "ft"
        elif condition[:3] == "BKN":
            toPrint += "\nBroken clouds at "
            toPrint += str(int(condition[3:]) * 100) + "ft"
        elif condition[:3] == "OVC":
            toPrint += "\nOvercast at "
            toPrint += str(int(condition[3:]) * 100) + "ft"
        elif condition[:3] == ("CLR" or "SKC"):
            toString += "\nClear skies"
        else:
            toPrint += "\nIndefinite ceiling with visibility up to "
            toPrint += str(int(condition[3:]) * 100) + "ft"
    return toPrint

def tempDewPoint(text):
    # Translate temp and dew point info from raw to readable
    # Format: TsT'T'T'sD'D'D'
    # NOTE: temps are reported in degrees celcius
    # T = string literal indicating "temperature"
    # s = sign of the temperature and dew point (1 for - or 0 for -)
    # T'T'T' = temperature (000-999)
    # D'D'D' = dew point temperature (000-999)
    
    # if temp and dew point is reported, get the information
    toPrint = ""
    
    # strip literal 'T'
    text = text[1:]

    # get temperature and its sign, then strip that info from mText
    if text[0] == '1':
        temp_Celcius = -1 * float(text[1:4])/10
        temp_Fahrenheit = temp_Celcius * (9/5) + 32
        toPrint += "\nTemperature: " + str(temp_Celcius) + "ºC, "
        toPrint += "%.f" % temp_Fahrenheit + "ºF"
    elif text[0] == '0':
        temp_Celcius = float(text[1:4])/10
        temp_Fahrenheit = temp_Celcius * (9/5) + 32
        toPrint += "\nTemperature: " + str(temp_Celcius) + "ºC, "
        toPrint += "%.f" % temp_Fahrenheit + "ºF"
    text = text[4:]

    # get dew point and its sign
    dp_Celcius = float(mText[1:])/10
    dp_Fahrenheit = dp_Celcius * (9/5) + 32.

    # for the sign, 1 = -, 0 = +
    if text[0] == '1':
        dp_Celcius *= -1
        dp_Fahrenheit = dp_Celcius * (9/5) + 32
        toPrint += "\nDew Point: " + str(dp_Celcius) + "ºC, "
        toPrint += "%.f" % dp_Fahrenheit + "ºF"
    elif text[0] == '0':
        toPrint += "\nDew Point: " + str(dp_Celcius) + "ºC, "
        toPrint += "%.f" % dp_Fahrenheit + "ºF"
    return toPrint

def altimeter(text):
    # Translates altimeter info from raw to readable
    # Format: APPPP
    # A = string literal indicating "Altimeter in inches of mercury"
    # PPPP = four digit group representing PP.PPin hg (decimal excluded)

    toPrint = ""
    reading = float(text[1:])/100
    toPrint = "\n\tAltimeter: %.2f" % reading + "in"
    return toPrint
