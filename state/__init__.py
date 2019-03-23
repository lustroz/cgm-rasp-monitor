import enum
import time
import nightscout
import database
import oled
import logging
from threading import Lock

logger = logging.getLogger('cgm')

defaultInterval = 30
emergencyInterval = 1

class State:
    Unknown = 0
    NoInternet = 1
    BluetoothCommand = 2
    DisplayValue = 10
    EmergencyValue = 11

    def __init__(self):
        self.state = State.Unknown
        self.settingTime = 0
        self.lock = Lock()

    def setState(self, s):
        with self.lock:
            self.state = s
            self.settingTime = time.time()

    def restoreState(self):
        with self.lock:
            if self.state == State.DisplayValue or self.state == State.EmergencyValue:
                return

            delta = time.time() - self.settingTime
            if delta > 3:
                self.state = State.DisplayValue

    def process(self, db):
        s = State.Unknown

        with self.lock:
            s = self.state

        # logger.info('process')
        if s == State.NoInternet:
            oled.drawState('No Internet')

        elif s == State.BluetoothCommand:
            oled.drawState('Bluetooth\ncommand')

        elif s == State.DisplayValue:
            rows = db.fetchEntries()

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


