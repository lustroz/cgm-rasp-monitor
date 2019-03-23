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
            self.cond.wait()            

    def notifier(self):
        while True:
            time.sleep(self.interval)
            self.cond.notifyAll()
       
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
