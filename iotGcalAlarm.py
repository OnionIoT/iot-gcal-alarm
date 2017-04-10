import os
import json
import urllib3
from icalendar import Calendar, Event


if __name__ == '__main__':
    # gets the location of this script
    dirName = os.path.dirname(os.path.abspath(__file__))

    # read the config file relative to the script location
    with open( '/'.join([dirName, 'config.json']) ) as f:
    	config = json.load(f)

    http = urllib3.PoolManager()

    # pull out the data string from the returned response
    rawIcs = http.request('GET', config['icalAddr']).data

    cal = Calendar.from_ical(rawIcs)

    for event in cal.walk() :
        print event.get('dtstart')
