import nightscout
import database
import time

database.createTable()

while True:
    print('\n***** retrieve server data *****\n')
    nightscout.getEntries()

    print('\n***** fetch entries from db *****\n')

    rows = database.fetchEntries()
    for row in rows:
        print(row)

    time.sleep(60)