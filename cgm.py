import data
import state
import nightscout
import database
import time
import oled
import btutil
import os
import logging
import logging.handlers
import asyncio
import threading
import RPi.GPIO as GPIO
import define
import tgutil
import setting

logger = logging.getLogger('cgm')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

file_max_bytes = 10 * 1024 * 1024
fileHandler = logging.handlers.RotatingFileHandler(filename='./cgm.log', maxBytes=file_max_bytes, backupCount=10)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

_state = state.State()
_data = data.Data()

startTime = time.time()

#init GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(define.KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(define.KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(define.KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(define.KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(define.KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(define.KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(define.KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(define.KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

class AsyncTask:

    def __init__(self):
        self.cond = threading.Condition()

    def bluetooth(self):
        try:
            while True:
                os.system('hciconfig hci0 piscan')
                btutil.listen(_state, self.cond)
                time.sleep(2)

        except Exception as e:
            logger.exception('bluetooth crashed. Error: %s', e)

    def process(self):
        try:
            db = database.Database()
            db.createTable()

            lastSentTime = 0

            while True:
                if _data.fetchData(_state, db):
                    _state.process(db)

                    curTime = int(time.time())
                    config = setting.getCurrent()

                    v = db.getDisplayValues()
                    if v['val'] > config['low_alarm'] and v['val'] < config['high_alarm']:
                        period = config['tg_normal_period']
                    else:
                        period = config['tg_urgent_period']

                    if curTime - lastSentTime > period * 60:
                        tgutil.sendLatestEntry(db)
                        lastSentTime = curTime

                else:
                     oled.drawState('No Internet')

                with self.cond:
                    self.cond.wait()     

                # reboot automatically in 3 hours..
                #elapsed = time.time() - startTime
                #if elapsed > 3 * 60 * 60:
                #    os.system('shutdown -r now')

        except Exception as e:
            logger.exception('process crashed. Error: %s', e)       

    def notifier(self):
        try:
            while True:
                _state.sleep()
                
                with self.cond:
                    self.cond.notifyAll()

        except Exception as e:
            logger.exception('notifier crashed. Error: %s', e)

    def keyHandler(self):
        try:
            while True:
                if not GPIO.input(define.KEY1_PIN):
                    _state.setKeyState(define.KEY1_PIN)

                time.sleep(1)

        except Exception as e:
            logger.exception('keyHandler crashed. Error: %s', e)
       
try:
    task = AsyncTask()

    threads = []
    t = threading.Thread(target=task.bluetooth)
    threads.append(t)
    t = threading.Thread(target=task.process)
    threads.append(t)
    t = threading.Thread(target=task.notifier)
    threads.append(t)
    t = threading.Thread(target=task.keyHandler)
    threads.append(t)

    logger.info('pharus started...')

    for t in threads:
        t.start()

    for t in threads:
        t.join()

except Exception as e:
    logger.exception('main crashed. Error: %s', e)
