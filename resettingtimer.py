
from threading import timer

class ResettingTimer(object):
"""
Resettable timer modified from 
http://stackoverflow.com/questions/24072765/timer-cannot-restart-after-it-is-being-stopped-in-python
"""
    def __init__(self, interval, f, *args, **kwargs):
        self.interval = interval
        self.f = f
        self.args = args
        self.kwargs = kwargs

        self.timer = None

    def callback(self):
        self.f(*self.args, **self.kwargs)
        self.start()

    def cancel(self):
        self.timer.cancel()

    def start(self):
        self.timer = Timer(self.interval, self.callback)
        self.timer.start()

    def reset(self):
        self.cancel()
        self.start()

