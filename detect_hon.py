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
import RPi.GPIO as GPIO
import hondetector.resettingtimer as rt


def blink_once():
    """TODO: don't sleep? And NB I hardcoded the GPIO output..."""
    GPIO.output(16, GPIO.HIGH)
    sleep(0.2)
    GPIO.output(16, GPIO.LOW)

def all_ok(timer):
    """Resets countdown timer"""
    timer.reset()
    print 'All good at time: ' + str(datetime.now())
    blink_once()

def fire_warning():
    """Only fires after timer interval"""
    print 'No activity recently. Fired at: ' + str(datetime.now())


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    in_channels = [15] # IR receiver
    out_channels = [16] # LED indicating passage

    GPIO.setup(in_channels, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(out_channels, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN) 


    #lame-o way of getting around not passing extra args to callback
    #
    callback = lambda channel, tm=timer: all_ok(tm)
    GPIO.add_event_detect(in_channels, GPIO.RISING,
                          callback=callback,
                          bouncetime=200)
    
    timer = rt.ResettingTimer(60 * 8, fire_warning)
    timer.start()

    try:
        # spin wheels unless ctrl+c
        while True:
            pass
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
