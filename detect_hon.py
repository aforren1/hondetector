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
from AlertEmail import AlertEmail
from AlertSMS import AlertSMS

def get_last_row_time(file_name):
    with open(file_name, 'r') as f:
        lastrow = None
        for lastrow in csv.reader(f): pass
        return datetime.strptime(lastrow[1], '%Y-%m-%d %H:%M:%S')

def blink_once():
    """TODO: don't sleep? And NB I hardcoded the GPIO output..."""
    GPIO.output(11, GPIO.HIGH)
    sleep(0.2)
    GPIO.output(11, GPIO.LOW)

def record_event():
    """Logs events; write immediately to file"""
    file_name = '/var/log/honlogs/honlog.csv'
    now = str(datetime.now())[0:19]
    print('Detection at: ' + now)
    with open(file_name, 'a') as appender:
        appendwriter = csv.writer(appender)
        appendwriter.writerow(['detect', now])
    blink_once()

def check_times(file_name, hrs_previous, notes):
    """Read most recent line of log, and see if it was within the last 4 hrs"""
    last_time = get_last_row_time(file_name)
    delta_time = datetime.now() - last_time
    if delta_time.seconds > hrs_previous * 60 * 60:
        fire_warning(notes, last_time, delta_time, file_name)

def fire_warning(notes, last_time, delta_time, file_name):
    """Do something if no activity during time windows"""
    message = ('Hon not detected recently (current time ' + str(datetime.now()) +
              '). Previous trigger at ' +
              str(last_time) + ', which was ' + str(delta_time) + ' ago.')
    print(message)
    with open(file_name, 'a') as appender:
        appendwriter = csv.writer(appender)
        appendwriter.writerow(['warning', now])
    notes[0].sendMessage(message)
    notes[1].sendMessage(message)

if __name__ == '__main__':

    file_name = '/var/log/honlogs/honlog.csv'
    if not os.path.isdir('/var/log/honlogs'):
        os.makedirs('/var/log/honlogs')
    
    if not os.path.isfile(file_name):
        with open(file_name, 'w') as new_log:
            new_writer = csv.writer(new_log)
            new_writer.writerow(['event_name', 'event_time'])

    GPIO.setmode(GPIO.BOARD)

    in_channels = 7 # IR receiver
    out_channels = 11 # LED indicating passage

    GPIO.setup(in_channels, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(out_channels, GPIO.OUT)

    GPIO.add_event_detect(in_channels, GPIO.RISING,
                          callback=record_event,
                          bouncetime=1000)
    # Make notifiers
    sms = AlertSMS()
    email = AlertEmail()
    notifiers = [sms, email]

    schedule.every().day.at("09:00").do(check_times, file_name=file_name, 
                                        hrs_previous=4, notes=notifiers)
    schedule.every().day.at("15:00").do(check_times, file_name=file_name, 
                                        hrs_previous=8, notes=notifiers)
    schedule.every().day.at("22:00").do(check_times, file_name=file_name, 
                                        hrs_previous=4, notes=notifiers)

    try:
        # spin wheels unless ctrl+c
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
