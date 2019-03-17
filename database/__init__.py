import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('cgm.db')

    def createTable(self):    
        c = self.conn.cursor()
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
        self.conn.commit()
        c.close()

    def getCurrentId(self):
        c = self.conn.cursor()
        c.execute('select current from id_generator where id = 1')
        row = c.fetchone()
        current = row[0]
        sql = 'insert or replace into id_generator values (?,?)'
        c.execute(sql, (1, current + 1))
        self.conn.commit()
        c.close()
        return current

    def insertEntry(self, origin, time, value, direction):
        c = self.conn.cursor()    
        sql = 'select id from entry where time = :Time'
        c.execute(sql, {'Time':time})
        rows = c.fetchall()
        if len(rows) == 0:
            id = self.getCurrentId()
        else:
            id = rows[0][0]
        sql = 'insert or replace into entry values (?,?,?,?,?)'
        c.execute(sql, (id, origin, time, value, direction))
        self.conn.commit()
        c.close()

    def fetchEntries(self):
        c = self.conn.cursor()
        sql = 'select * from entry order by time desc limit 30'
        c.execute(sql)
        return c.fetchall()



