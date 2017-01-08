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

import RPi.GPIO as GPIO
from datetime import datetime
import resettingtimer as rt

GPIO.setmode(GPIO.BOARD)

in_channels = [15] # IR receiver
out_channels = [16] # LED indicating passage

GPIO.setup(in_channels, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(out_channels, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) 

def all_ok(channel, timer):
    timer.reset()
    print('All good at time: ' + str(datetime.now()))

def fire_warning():
    print('No activity recently. Fired at: ' + str(datetime.now()))

t = rt.ResettingTimer(60 * 8, fire_warning)

GPIO.add_event_detect(in_channels, GPIO.RISING,
                      callback = all_ok, 
                      bouncetime = 200)

# spin our wheels
while True:
    pass