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

    if len(rows) > 1:
        delta = rows[0][3] - rows[1][3]
    else:
        delta = 0

    if len(rows) > 0:
        latest = rows[0]
        oled.draw(latest[1], latest[2], latest[3], latest[4], delta)

    time.sleep(60)
