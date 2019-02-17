import nightscout
import database
import time
import oled

database.createTable()

while True:
    print('\n***** retrieve server data *****\n')
    nightscout.getEntries()

    print('\n***** fetch entries from db *****\n')

    rows = database.fetchEntries()
    for row in rows:
        print(row)

    if len(rows) > 0:
        latest = rows[0]
        oled.draw(latest.origin, latest.time, latest.value, latest.direction)

    time.sleep(60)