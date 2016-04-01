'''
AUTHOR: Byron Himes
MODIFIED: 31 March 2016
DESCRIPTION: A script to scrape a METAR string from the Aviation Digital
    Data Service (ADDS) using a user-provided weather station ID (e.g. KSGF)
FILES: metarScrape.py
'''

from lxml import html
import requests

def getReport(s = None):
    url = 'https://www.aviationweather.gov/adds/metars/?station_ids='+s+'&std_trans=standard&chk_metars=on&hoursStr=most+recent+only&submitmet=Submit'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    metar = tree.xpath('//font[@face="Monospace,Courier"]/text()')
    return(metar[0])
