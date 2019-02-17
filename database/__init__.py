import sqlite3

conn = sqlite3.connect('cgm.db')

def createTable():    
    c = conn.cursor()
    c.execute('''create table if not exists id_generator (
        id integer primary key, 
        current integer
    )''')
    c.execute('insert or ignore into id_generator values (1, 1)')
    c.execute('''create table if not exists entry (
        id integer primary key,
        origin text,
        time integer,
        value integer,
        direction text
    )''')
    conn.commit()
    c.close()

def getCurrentId():
    c = conn.cursor()
    c.execute('select current from id_generator where id = 1')
    row = c.fetchone()
    current = row[0]
    sql = 'insert or replace into id_generator values (?,?)'
    c.execute(sql, (1, current + 1))
    conn.commit()
    c.close()
    return current

def insertEntry(origin, time, value, direction):
    c = conn.cursor()    
    sql = 'select id from entry where time = :Time'
    c.execute(sql, {'Time':time})
    rows = c.fetchall()
    if len(rows) == 0:
        id = getCurrentId()
    else:
        id = rows[0][0]
    sql = 'insert or replace into entry values (?,?,?,?,?)'
    c.execute(sql, (id, origin, time, value, direction))
    conn.commit()
    c.close()

def fetchEntries():
    c = conn.cursor()
    sql = 'select * from entry order by time desc limit 30'
    c.execute(sql)
    return c.fetchall()



