import timeit


class MasterClock():
    """
    class is responsible for timing every round
    """

    def __init__(self):
        """
        constructor initializes neccessary variables
        """

        self.start = 0.0
        self.displayed = 0.0
        self.accurate = 0.0000

    def run_timer(self):
        """
        function to start the timer
        """

        self.start = timeit.default_timer()

    def read_displayed(self):
        """
        function to read timer for gui

        Returns:
            float: one decimal float of current timer value
        """

        self.displayed = round(timeit.default_timer() - self.start, 1)
        return self.displayed

    def read_accurate(self):
        """
        function to read timer for gamehandler

        Returns:
            float: four decimal float of current timer value
        """

        self.accurate = round(timeit.default_timer() - self.start, 4)
        return self.accurate


clock = MasterClock()
