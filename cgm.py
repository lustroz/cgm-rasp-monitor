import data
import state
import nightscout
import database
import time
import oled
import btutil
import logging
import logging.handlers
import asyncio
import threading
import RPi.GPIO as GPIO

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

#init GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

class AsyncTask:

    def __init__(self):
        self.cond = threading.Condition()
        self.interval = 30

    def bluetooth(self):
        while True:
            btutil.listen(_state, self.cond)
            time.sleep(2)

    def process(self):
        db = database.Database()
        db.createTable()

        while True:
            _data.fetchData(_state, db)
            _state.process(db)

            with self.cond:
                self.cond.wait()            

    def notifier(self):
        while True:
            _state.sleep()
            
            with self.cond:               
                self.cond.notifyAll()

    def keyHandler(self):
        while True:
            if GPIO.input(KEY1_PIN):
                _state.setKeyState(KEY1_PIN)
       
try:
    task = AsyncTask()

    threads = []
    t = threading.Thread(target=task.bluetooth)
    threads.append(t)
    t = threading.Thread(target=task.process)
    threads.append(t)
    t = threading.Thread(target=task.notifier)
    threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

except Exception as e:
    logger.exception('main crashed. Error: %s', e)
