import nightscout
import time

while True:
    nightscout.getEntries()

    time.sleep(60)