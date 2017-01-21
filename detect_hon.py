"""
Pin info:
pin 1 is 3v3 DC, 2 and 4 are 5v
pins 6, 9, 14 are GND

LED Circuit:
out_pin -> LED (long leg) -> LED (short leg) -> 
300ohm resistor -> (digital?) GND

IR Receiver input:
signal wire -> (10kOhm resistor if no internal pullup)  -> in_pin
"""
from datetime import datetime
from time import sleep
import csv
import schedule
import RPi.GPIO as GPIO

def get_last_row(filename):
    with open(filename, 'r') as f:
        lastrow = None
        for lastrow in csv.reader(f): pass
        return lastrow

def blink_once():
    """TODO: don't sleep? And NB I hardcoded the GPIO output..."""
    GPIO.output(23, GPIO.HIGH)
    sleep(0.2)
    GPIO.output(23, GPIO.LOW)

def record_event(evt_log):
    """Logs events; write immediately to file"""
    dt = datetime.now()
    print 'All good at time: ' + str(dt)
    # blink_once()
    return evt_log

def check_times(evt_log):
    """Read most recent line of log, and see if it was within the last 4 hrs"""
    pass


def fire_warning():
    """Only fires after timer interval"""
    print 'No activity recently. Fired at: ' + str(datetime.now())

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    in_channels = [18] # IR receiver
    out_channels = [23] # LED indicating passage

    GPIO.setup(in_channels, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(out_channels, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) 

    #lame-o way of getting around not passing extra args to callback
    #
    callback = lambda channel, event_log=log_today: record_event(event_log)
    GPIO.add_event_detect(in_channels, GPIO.FALLING,
                          callback=callback,
                          bouncetime=200)

    event_log = []

    schedule.every().minute.do(write_events_elsewhere, evt_log=event_log)

    try:
        # spin wheels unless ctrl+c
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
