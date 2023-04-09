# timeit libary used for accurate readings
import timeit

# use a class structue for timer


class MasterClock():
    def __init__(self):
        self.start = 0.0

    # timer start marked for self.start
    def runClassicTimer(self):
        self.start = timeit.default_timer()
        self.readDisplayed()

    # one decimal point display for player
    def readDisplayed(self):
        self.displayed = round(timeit.default_timer() - self.start, 1)
        return self.displayed

    # four decimal option for game handler
    def readAccurate(self):
        self.accurate = round(timeit.default_timer() - self.start, 4)
        return self.accurate


clock = MasterClock()
