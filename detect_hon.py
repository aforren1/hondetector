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
import os
from datetime import datetime
from time import sleep
import csv
import schedule
import RPi.GPIO as GPIO

def get_last_row_time(file_name):
    with open(file_name, 'r') as f:
        lastrow = None
        for lastrow in csv.reader(f): pass
        return datetime.strptime(lastrow[1], '%Y-%m-%d %H:%M:%S')

def blink_once():
    """TODO: don't sleep? And NB I hardcoded the GPIO output..."""
    GPIO.output(23, GPIO.HIGH)
    sleep(0.2)
    GPIO.output(23, GPIO.LOW)

def record_event(file_name):
    """Logs events; write immediately to file"""
    with open(file_name, 'a') as appender:
        appendwriter = csv.writer(appender)
        appendwriter.writerow(['detect', str(datetime.now())[0:19]])
    blink_once()

def check_times(file_name):
    """Read most recent line of log, and see if it was within the last 4 hrs"""
    last_time = get_last_row_time(file_name)
    delta_time = datetime.now() - last_time
    if delta_time.seconds > 14400: # four hours
        fire_warning()

def fire_warning():
    """Do something if no activity during time windows"""
    print 'No activity recently. Fired at: ' + str(datetime.now())

if __name__ == '__main__':

    file_name = 'logs/honlog.csv'
    if not os.path.isdir('logs'):
        os.makedirs('logs')
    
    if not os.path.isfile(file_name):
        with open(file_name, 'w') as new_log:
            new_writer = csv.writer(new_log)
            new_writer.writerow(['event_name', 'event_time'])

    GPIO.setmode(GPIO.BCM)

    in_channels = [18] # IR receiver
    out_channels = [23] # LED indicating passage

    GPIO.setup(in_channels, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(out_channels, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

    #lame-o way of getting around not passing extra args to callback
    #
    callback = lambda channel, file_name: record_event(file_name)
    GPIO.add_event_detect(in_channels, GPIO.FALLING,
                          callback=record_event,
                          bouncetime=200)

    schedule.every().day.at("09:00").do(check_times, file_name=file_name)
    schedule.every().day.at("22:00").do(check_times, file_name=file_name)

    try:
        # spin wheels unless ctrl+c
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
