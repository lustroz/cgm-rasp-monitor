import enum
import nightscout
import time
import wifi
import setting

class Data:
    def __init__(self):
       return

    def fetchData(self, state, db):
        
        if wifi.checkNetwork():
            state.setState(state.DisplayValue)
            src = setting.getSourceType()
            if src == 'nightscout':
                nightscout.getEntries(state, db)
            elif src == 'dexcomshare':
                pass
        else:
            state.setState(state.NoInternet)
            
        
