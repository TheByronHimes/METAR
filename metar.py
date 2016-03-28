'''
AUTHOR: Byron Himes
MODIFIED: 28 March 2016
DESCRIPTION: Takes a METAR reading as input and outputs the interpretation (meaning).
FILES: metar.py
'''

# define a dictionary to label the fields dynamically
fields = {}

def getReading():
    reading = input("Enter METAR reading: ")
    return reading

def isReportType(key, d):
    pass

def isStationID(key, d):
    pass


if __name__ == "__main__":

    # get raw metar reading
    metar_reading = getReading()

    # populate the fields dictionary
    for i in (0, len(metar_reading)):
        fields[i] = ""



    
