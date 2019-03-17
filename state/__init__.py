import enum
import time
import nightscout
import database
import oled

defaultInterval = 30
emergencyInterval = 1

class State:
    Unknown = 0
    NoInternet = 1
    DisplayValue = 10
    EmergencyValue = 11

    def __init__(self):
        self.state = State.DisplayValue
        self.interval = defaultInterval
        self.settingTime = 0

    def setState(self, s):
        self.state = s
        self.interval = 0
        self.settingTime = time.time()

    def restoreState(self):
        if self.state == State.Unknown:
            delta = time.time() - settingTime
            if delta > 3:
                self.state = State.DisplayValue

    def process(self):
        if self.state == State.NoInternet:
            oled.drawState('No Internet')

        elif self.state == State.DisplayValue:
            rows = database.fetchEntries()

            if len(rows) > 1:
                delta = rows[0][3] - rows[1][3]
            else:
                delta = 0

            if len(rows) > 0:
                latest = rows[0]
                oled.draw(latest[1], latest[2], latest[3], latest[4], delta)

        else: 
            oled.drawState('Unknown')

        self.restoreState()

        if self.state == State.EmergencyValue:
            self.interval = emergencyInterval
        else:
            self.interval = defaultInterval


