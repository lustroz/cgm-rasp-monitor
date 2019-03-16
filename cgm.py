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

async def main():

    while True:
        state.processCurrentState()
        
try:
    loop = asyncio.get_event_loop()

    tasks = asyncio.gather(bluetooth.listen(), data.fetchData(), main())

    loop.run_until_complete(tasks)

except Exception as e:
    logger.exception('main crashed. Error: %s', e)
