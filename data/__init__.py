import enum
import nightscout
import time
import wifi

class Data:
    DexcomShare = 0
    Nightscout = 1

    def __init__(self):
        self.mode = Data.Nightscout

    def fetchData(self, state):
        if not wifi.checkNetwork():
            state.setState(state.NoInternet)
            
        if self.mode == Data.DexcomShare:
            pass
        else:
            nightscout.getEntries()

