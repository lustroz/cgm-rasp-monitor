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

    def __init__(self):
        self.state = State.Unknown
        self.emergency = False
        self.dimmed = False
        self.settingTime = 0
        self.lock = Lock()

    def setState(self, s):
        with self.lock:
            self.state = s
            self.settingTime = time.time()

    def restoreState(self):
        with self.lock:
            if self.state == State.DisplayValue:
                return

            delta = time.time() - self.settingTime
            if delta > 3:
                self.state = State.DisplayValue

    def process(self, db):
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
                val = latest[3]

                color = 255

                with self.lock:
                    if val < 80 or val > 100:
                        self.emergency = True

                        if self.dimmed:
                            color = 0
                        else:
                            color = 255

                        self.dimmed = not self.dimmed
                    else:
                        self.emergency = False

                oled.draw(latest[1], latest[2], val, latest[4], delta, color)

        else: 
            oled.drawState('Unknown')

        self.restoreState()

    def sleep(self):
        with self.lock:
            e = self.emergency

        if e:
            time.sleep(emergencyInterval)
        else:
            time.sleep(defaultInterval)


