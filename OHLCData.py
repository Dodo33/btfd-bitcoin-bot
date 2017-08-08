import datetime

class OHLCData:
    def __init__(self, date = datetime.datetime(2000, 1, 1, 1, 1, 1), open = 0, high = 0, low = 0, close = 0):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    def __str__(self):
        return "[ " + str(self.date) + ", " + str(self.open) + ", "+ str(self.high) + ", " + str(self.low) + ", " + str(self.close) + " ]"

    def __repr__(self):
        return self.__str__()

    def toCsvString(self):
        #self.date.strftime("%Y-%m-%d %H:%M:%S")
        return str(self.date) + "," + str(self.open) + "," + str(self.high) + "," + str(self.low) + "," + str(self.close)

