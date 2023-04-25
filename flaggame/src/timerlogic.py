# MODULE DESCRIPTION

# timerlogic enables a master instance for game timings

# both gamehandler and gui can therefore utilize same clock

import timeit  # timeit libary used for accurate readings

# use a class structue for timer


class MasterClock():
    def __init__(self):
        self.start = 0.0
        self.displayed = 0.0
        self.accurate = 0.0000

    # timer start (round start point)
    def run_classic_timer(self):
        self.start = timeit.default_timer()

    # one decimal point display for player
    def read_displayed(self):
        self.displayed = round(timeit.default_timer() - self.start, 1)
        return self.displayed

    # accurate four decimal option for game handler
    def read_accurate(self):
        self.accurate = round(timeit.default_timer() - self.start, 4)
        return self.accurate


# run the instance
clock = MasterClock()
