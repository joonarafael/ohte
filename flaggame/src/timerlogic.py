import timeit
import time
#import gui

class MasterClock():
    def __init__(self):
        self.start = 0.0
        
    def runClassicTimer(self):
        self.start = timeit.default_timer()
        self.readDisplayed()
    
    def readDisplayed(self):
        self.displayed = round(timeit.default_timer() - self.start, 1)
        return self.displayed
    
    def readAccurate(self):
        self.accurate = round(timeit.default_timer() - self.start, 4)
        return self.accurate

clock = MasterClock()