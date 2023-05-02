import timeit


class MasterClock():
    """
    master clock instance
    """

    def __init__(self):
        """
        initialize all neccessary variables
        """

        self.start = 0.0

    def run_timer(self):
        """
        start the timer (every round)
        """

        self.start = timeit.default_timer()

    def read_displayed(self):
        """
        read the timer for gui

        Returns:
            float: one decimal float of current timer value
        """

        return round(timeit.default_timer() - self.start, 1)

    def read_accurate(self):
        """
        read the timer for gamehandler

        Returns:
            float: four decimal float of current timer value
        """

        return round(timeit.default_timer() - self.start, 4)


clock = MasterClock()
