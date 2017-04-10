# Online Calendar Buzzer Alarm for Onion Omega2/2+

This project sets up a service on the Omega to check an online calendar, and sets up a buzzer to ring on time for events with an appropriate keyword.

## Requirements

* Buzzer circuit
* pip
* Python packages:
	* urllib3, python-crontab, icalendar

## Setup

clone into `/root` and move `alarm.sh` to root as well. Add the location of the ics calendar of your choice to `config.json` and it's ready to run.
