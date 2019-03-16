import enum
import time
import nightscout
import database
import oled

class State(enum.Enum):
    Unknown = 0
    NoInternet = 1
    DisplayValue = 10
    EmergencyValue = 11

state = State.Unknown

defaultInterval = 30
emergencyInterval = 1
interval = defaultInterval
settingTime = 0

def setState(s):
    state = s
    interval = 0
    settingTime = time.time()

def restoreState():
    if state == State.Unknown:
        delta = time.time() - settingTime
        if delta > 3:
            state = State.DisplayValue

def processCurrentState():
    if state == State.NoInternet:
        oled.drawState('No Internet')

    elif state == State.DisplayValue:

        rows = datebase.fetchEntries()

        if len(rows) > 1:
            delta = rows[0][3] - rows[1][3]
        else:
            delta = 0

        if len(rows) > 0:
            latest = rows[0]
            oled.draw(latest[1], latest[2], latest[3], latest[4], delta)

    else: 
        oled.drawState('Unknown')

    time.sleep(interval)

    if state == State.EmergencyValue:
        interval = emergencyInterval
    else:
        interval = defaultInterval


