import enum
import time
import nightscout
import database
import oled
import logging
from threading import Lock
import os
import define
import setting

logger = logging.getLogger('cgm')

defaultInterval = 5
emergencyInterval = 1

class State:
    Unknown = 0

    NoInternet = 1
    DisplayValue = 2
    InvalidParam = 3

    BT_Connected    = 100
    BT_SetupWifi    = 101
    BT_Reboot       = 102
    BT_SourceChange = 103
    BT_NightScout   = 104
    BT_DexcomShare  = 105

    def __init__(self):
        self.state = State.Unknown
        self.cmdState = State.Unknown

        self.emergency = False
        self.dimmed = False
        self.settleTime = 0
        self.lock = Lock()
        self.shouldReboot = False

    def setState(self, s):
        with self.lock:
            self.state = s

    def setCmdState(self, s):
        with self.lock:
            self.cmdState = s
            self.settleTime = time.time()

    def restoreState(self):
        with self.lock:
            if self.cmdState == State.Unknown or self.cmdState == State.BT_Connected: 
                return

            delta = time.time() - self.settleTime
            if delta > 2:
                self.cmdState = State.BT_Connected

    def setKeyState(self, key):
        with self.lock:
            if key == define.KEY1_PIN:
                self.shouldReboot = True

    def process(self, db):
        with self.lock:
            s = self.state
            cs = self.cmdState

        srcType = setting.getSourceType()
        if srcType == 'nightscout':
            srcName = 'NightScout'
        else:
            srcName = 'DexcomShare'

        if cs == State.BT_Connected:
            #logger.info('bt connected')
            oled.drawState('Bluetooth\nConnected')

        elif cs == State.BT_SetupWifi:
            #logger.info('bt wifi')
            oled.drawState('Setup Wifi')

        elif cs == State.BT_Reboot:
            #logger.info('bt reboot')
            oled.drawState('Reboot')

        elif cs == State.BT_SourceChange:
            #logger.info('bt source_change')
            oled.drawState('Source Change')

        elif cs == State.BT_NightScout:
            #logger.info('bt nightscout')
            oled.drawState('NightScout\nAddress')

        elif cs == State.BT_DexcomShare:
            #logger.info('bt dexcomshare')
            oled.drawState('DexcomShare\nAddress')

        elif s == State.NoInternet:
            #logger.info('no internet')
            oled.drawState('No Internet')

        elif s == State.InvalidParam:
            oled.drawState(srcName + '\nInvalid Parameter')

        elif s == State.DisplayValue:
            r = db.getDisplayValues()
            if r['val'] > 0:
                color = 255
                with self.lock:
                    if r['val'] < setting.getLowAlarm() or r['val'] > setting.getHighAlarm() or (r['elapsed'] / 60) > setting.getNoSignalAlarm():
                        self.emergency = True

                        if self.dimmed:
                            color = 0
                        else:
                            color = 255

                        self.dimmed = not self.dimmed
                    else:
                        self.emergency = False

                oled.draw(srcType, r['elapsed'], r['val'], r['direction'], r['delta'], color)

        else: 
            oled.drawState('Unknown')

        self.restoreState()

        with self.lock:
            if self.shouldReboot:
                os.system("shutdown -r now")
                self.shouldReboot = False

    def sleep(self):
        # with self.lock:
        #     e = self.emergency

        # if e:
            time.sleep(emergencyInterval)
        # else:
        #     time.sleep(defaultInterval)


