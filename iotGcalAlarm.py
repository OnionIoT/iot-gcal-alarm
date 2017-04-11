import os
import json
import urllib3
import pytz
from datetime import datetime
from crontab import CronTab
from icalendar import Calendar, Event


if __name__ == '__main__':
    # reads config based off the full path of the script for cron compatibility
    dirName = os.path.dirname(os.path.abspath(__file__))
    with open( '/'.join([dirName, 'config.json']) ) as f:
    	config = json.load(f)

    http = urllib3.PoolManager()

    # gets the icalendar and converts it to a python readable object
    rawIcs = http.request('GET', config['icalAddr']).data
    cal = Calendar.from_ical(rawIcs)

    # cron object creation that will handle job creation and deletion
    cron = CronTab(user='root')

    # gets a list of buzzer alarmed cronjobs
    buzzerAlarmsList = cron.find_comment('SET_BUZZER')

    # current time for reference
    timeNow = datetime.now()
    timeNow = pytz.utc.localize(timeNow) # convert to timezone-aware datetime object

    # loops over every event in the calendar
    for event in cal.walk() :
        dtstart = event.get ('dtstart')
        summary = event.get ('summary')

        # recurrance rules variable
        # recurrance = event.get ('rrule')

        # check for events that match buzzer criteria:
        #    * has string 'SET_BUZZER'
        #    * has summary
        #    * has time
        if (summary is not None and dtstart is not None and summary.find ('SET_BUZZER') is not -1):
            # converts ics formatted time to datetime object
            timeOfEvent = dtstart.from_ical(dtstart)

            # create a string in crontab format from the event time data
            cronTimeEvent = str(timeOfEvent.minute) + ' ' + str(timeOfEvent.hour) + ' ' + str(timeOfEvent.day) + ' ' + str(timeOfEvent.month) + ' *'

            # duplicate job flag
            isNewJob = True

            for job in buzzerAlarmsList:
                cronTimeJob = str(job.slices)
                # jobDesc =  job.render()
                if (timeNow > timeOfEvent):           # checks for old job
                    isNewJob = False                  # marks the job as already created
                    # print 'old job: ' + jobDesc
                    cron.remove(job)
                    break

                if (cronTimeJob == cronTimeEvent):    # checks for duplicate job
                    isNewJob = False                  # marks the job as already created
                    # print 'duplicate: ' + jobDesc
                    break

            if (isNewJob):                            # checks for the created flag
                job = cron.new (command='/bin/sh /root/alarm.sh')
                job.setall(timeOfEvent)
                job.set_comment('SET_BUZZER')
                # print 'new job: ' + job.render()

    cron.write()                             # finalize cron tab with new/deleted jobs
    os.system("/etc/init.d/cron restart")    # restart crond for changes to take effect

