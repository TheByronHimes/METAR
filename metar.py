'''
AUTHOR: Byron Himes
MODIFIED: 11 April 2016
DESCRIPTION: A class to parse and house METAR report information
FILES: metar.py
TODO: Implement present weather group
'''
import re

class Metar:
    def __init__(self, report):
        self.stationID = ""
        self.dateTime = ""
        self.modifier = ""
        self.wind = ""
        self.visibility = ""
        self.runway = ""
        self.presentWeather = []
        self.sky = []
        self.tempDewPoint = ""
        self.altimeter = ""
        self.setup(report)

    def setup(self, reportText):
        # Station ID
        idPattern = re.compile('[A-Z]{4}\s')
        match = re.search(idPattern, reportText)
        if match != None:
            self.stationID = match.group()

        # Date and Time
        dtPattern = re.compile('([0-3]\d)([0-2]\d[0-5]\d)Z')
        match = re.search(dtPattern, reportText)
        if match!= None:
            self.dateTime = match.group()

        # Report Modifier Code
        modPattern = re.compile('(AUTO|COR)')
        match = re.search(modPattern, reportText)
        if match!= None:
            self.modifier = match.group()
        
        # Wind Group
        windPattern = re.compile(
            '((VRB|[0-3]\d{1,2})(\d{2,3})(G\d{2,3})?KT|00000KT)(\s[0-3]\d{1,2}V[0-3]\d{1,2})?'
        )
        match = re.search(windPattern, reportText)
        if match != None:
            self.wind = match.group()

        # Visibility Group
        visPattern = re.compile(
            'M?(([1-9]\s[1-9]/[1-9])|([1-9]/[1-9])|(\d{1,2}))SM'
        )
        match = re.search(visPattern, reportText)
        if match != None:
            self.visibility = match.group()

        # Runway Visibility
        rvPattern = re.compile(
            '(R\d{2}[CRL]?/\d{4}FT)|(R\d{2}[CRL]?/\d{4}V\d{4}FT)'
        )
        match = re.search(rvPattern, reportText)
        if match != None:
            self.runway = match.group()

        # Present weather group not implemented

        # Sky Condition Groups
        fewPattern = re.compile('FEW\d{3}')
        sctPattern = re.compile('SCT\d{3}')
        bknPattern = re.compile('BKN\d{3}')
        ovcPattern = re.compile('OVC\d{3}')
        vertPattern = re.compile('VV\d{3}')
        clearPattern = re.compile('SKC|CLR')
        fewMatches = re.findall(fewPattern, reportText)
        sctMatches = re.findall(sctPattern, reportText)
        bknMatches = re.findall(bknPattern, reportText)
        ovcMatches = re.findall(ovcPattern, reportText)
        vertMatches = re.findall(vertPattern, reportText)
        clearMatches = re.findall(clearPattern, reportText)
        self.sky = fewMatches + sctMatches + bknMatches + ovcMatches + vertMatches + clearMatches

        # Temperature and Dew Point
        tdPattern = re.compile('T[01]\d{3}[01]\d{3}')
        match = re.search(tdPattern, reportText)
        if match != None:
            self.tempDewPoint = match.group()

        # Altimeter
        altPattern = re.compile('A\d{4}')
        match = re.search(altPattern, reportText)
        if match != None:
            self.altimeter = match.group()

    def getStationID(self):
        return self.stationID

    def getDateTime(self):
        return self.dateTime

    def getModifier(self):
        return self.modifier

    def getWind(self):
        return self.wind

    def getVisibility(self):
        return self.visibility

    def getRunway(self):
        return self.runway

    def getPresentWeather(self):
        # NOT YET IMPLEMENTED
        return None

    def getSky(self):
        return self.sky

    def getTempDewPoint(self):
        return self.tempDewPoint

    def getAltimeter(self):
        return self.altimeter
