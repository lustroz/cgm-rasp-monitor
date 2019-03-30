import enum
import time
import nightscout
import database
import oled
import logging
from threading import Lock
import os

logger = logging.getLogger('cgm')

defaultInterval = 30
emergencyInterval = 1

#GPIO define
RST_PIN        = 25
CS_PIN         = 8
DC_PIN         = 24
KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13
KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

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
        self.shouldReboot = False

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

    def setKeyState(self, key):
        with self.lock:
            if key == KEY1_PIN:
                self.shouldReboot = True

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
                elapsed = int(time.time()) - latest[2] / 1000

                with self.lock:
                    if val < 80 or val > 170 or (elapsed / 60) > 15:
                        self.emergency = True

                        if self.dimmed:
                            color = 0
                        else:
                            color = 255

                        self.dimmed = not self.dimmed
                    else:
                        self.emergency = False

                oled.draw(latest[1], elapsed, val, latest[4], delta, color)

        else: 
            oled.drawState('Unknown')

        self.restoreState()

        with self.lock:
            if self.shouldReboot:
                os.system("shutdown -r now")
                self.shouldReboot = False

    def sleep(self):
        with self.lock:
            e = self.emergency

        if e:
            time.sleep(emergencyInterval)
        else:
            time.sleep(defaultInterval)


