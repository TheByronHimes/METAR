'''
AUTHOR: Byron Himes
MODIFIED: 25 March 2016
DESCRIPTION: Takes a METAR reading as input and outputs the interpretation (meaning).
FILES: metar.py
'''

def getReading():
    reading = input("Enter METAR reading: ")
    return reading

def getReportType(metar):
    pass

def getStationID(metar):
    pass

def interpret(metar):
    # Format is as follows:
    # TYPE ID TIME WIND VIS WX SKY T/TD ALT REMARK


if __name__ == "__main__":
    metar_reading = getReading()
    
