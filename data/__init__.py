import enum
import nightscout
import time
import wifi
import state

class Mode(enum.Enum):
    DexcomShare = 0
    Nightscout = 1

mode = Mode.Nightscout

async def fetchData():
    while True:
        if not wifi.checkNetwork():
            state.setState(state.State.NoInternet)
            
        if mode == Mode.DexcomShare:
            print('dexcom')
        else:
            nightscout.getEntries()

        time.sleep(30)
