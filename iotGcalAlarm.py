import os
import json
import urllib3
from datetime import datetime
from crontab import CronTab
from icalendar import Calendar, Event, vDDDTypes


if __name__ == '__main__':
    # gets the location of this script
    dirName = os.path.dirname(os.path.abspath(__file__))

    # read the config file relative to the script location
    with open( '/'.join([dirName, 'config.json']) ) as f:
    	config = json.load(f)

    http = urllib3.PoolManager()

    # pull out the data string from the returned response
    rawIcs = http.request('GET', config['icalAddr']).data

    # converting the calendar to readable format
    cal = Calendar.from_ical(rawIcs)

    cron = CronTab(user='root')

    # check the time for reference
    timeNow = datetime.now()

    for event in cal.walk() :
        timeIcsRaw = event.get ('dtstart')
        timeOfEvent = timeIcsRaw.from_ical(timeIcsRaw)
        summary = event.get ('summary')

        # this variable will contain recurrance rules of the event
        # recurrance = event.get ('rrule')

        # the keyword used to detect which events need a buzzer is 'SET_BUZZER'
        if (summary is not None):
            if (summary.find ('SET_BUZZER') is not -1): # checks for the keyword
                if (timeNow < timeOfEvent):             # make sure event is in the future
                    job = cron.new (command='/bin/sh /root/alarm.sh')
                    job.setall(timeOfEvent)
                else:                                   # lazy way to remove uneeded entries
                    cron.remove_all(time = timeOfEvent.minute + timeOfEvent.hour + timeOfEvent.day + timeOfEvent.month)


    cron.write()

