import enum
import nightscout
import time
import wifi

class Data:
    DexcomShare = 0
    Nightscout = 1

    def __init__(self):
        self.mode = Data.Nightscout

    def fetchData(self, state, db):
        if wifi.checkNetwork():
            if self.mode == Data.DexcomShare:
                pass
            else:
                nightscout.getEntries(state, db)
        else:
            state.setState(state.NoInternet)
            
        
