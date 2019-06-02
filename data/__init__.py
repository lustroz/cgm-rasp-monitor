import enum
import nightscout
import time
import wifi

class Data:
    DexcomShare = 0
    Nightscout = 1

    def __init__(self):
       return

    def fetchData(self, state, db):
        if wifi.checkNetwork():
            nightscout.getEntries(state, db)
        else:
            state.setState(state.NoInternet)
            
        
