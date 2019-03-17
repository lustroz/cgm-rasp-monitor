import data
import state
import nightscout
import database
import time
import oled
import bluetooth
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

database.createTable()

_state = state.State()
_data = data.Data()

class AsyncTask:
    def fetchData(self):
        _data.fetchData(_state)
        threading.Timer(30, self.fetchData).start()

    def process(self):
        _state.process()
        threading.Timer(_state.interval, self.process).start()
       
try:
    task = AsyncTask()
    task.fetchData()
    task.process()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([bluetooth.listen()]))

except Exception as e:
    logger.exception('main crashed. Error: %s', e)
