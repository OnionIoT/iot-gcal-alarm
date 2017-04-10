import os
import json
import urllib3
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
    print cal


    # cron = CronTab(user='root')

    for event in cal.walk() :
        timeRaw = event.get ('dtstart')
        summary = event.get ('summary')

        # this variable will contain recurrance rules of the event
        recurrance = event.get ('rrule')
        print summary

        # the keyword used to detect which events need a buzzer is 'SET_BUZZER'
        if (summary is not None):
            if (summary.find ('SET_BUZZER') is not -1):
                t = timeRaw.split (' ')

                date = t[0].split ('-')
                month = int (date[1])
                day = int (date[2])

                time = t[1].split ('+')
                time = time.split (':')
                hour = int (time[0])
                minute = int (time[1])

            #     job = cron.new (command='/usr/bin/echo gpioctl dirout-high 13')
            #     job.month.on (month)
            #     job.day.on (day)
            #     job.hour.on (hour)
            #     job.minute.on (minute)
            #     job.write()


