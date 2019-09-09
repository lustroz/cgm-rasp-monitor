import enum
import nightscout
import time
import wifi
import setting
import dexcomshare

lastFetchTime = 0
fetchPeriod = 60

class Data:
    def __init__(self):
       return

    def fetchData(self, state, db):
        
        if wifi.checkNetwork():           

            global lastFetchTime

            curTime = int(time.time())
            if curTime - lastFetchTime < fetchPeriod:
                return True

            src = setting.getSourceType()
            if src == 'nightscout':
                nightscout.getEntries(state, db)
            elif src == 'dexcomshare':
                dexcomshare.getEntries(state, db)

            lastFetchTime = curTime

            return True

        else:
            state.setState(state.NoInternet)

            return False
            
        
