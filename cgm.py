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

database.createTable()

async def main():

    while True:
        # print('\n***** retrieve server data *****\n')
        nightscout.getEntries()

        # print('\n***** fetch entries from db *****\n')

        rows = database.fetchEntries()
        # for row in rows:
        #     print(row)

        if len(rows) > 1:
            delta = rows[0][3] - rows[1][3]
        else:
            delta = 0

        if len(rows) > 0:
            latest = rows[0]
            oled.draw(latest[1], latest[2], latest[3], latest[4], delta)

        time.sleep(60)


try:
    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.gather(bluetooth.listen(), main()))

except Exception as e:
    logger.exception('main crashed. Error: %s', e)
