import sqlite3

class Database():


    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS "lab" (
                                        "id"  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        "type" TEXT,
                                        "price" REAL,
                                        "date" TEXT,
                                        "term" INTEGER);''')


    def fetch(self):
        string = 'SELECT type, price, date, term FROM lab;'
        self.cur.execute(string)
        rows = self.cur.fetchall()
        return rows


    def insert(self, type, price, date, term):
        string = f'''INSERT INTO lab(type, price, date, term) 
                     VALUES ("{type}", {price}, "{date}", {term});
                    '''
        self.cur.execute(string)
        self.conn.commit() 


    def get_max(self):
        string = '''SELECT type, price, date, term 
                   FROM lab
                   WHERE price = (SELECT MAX(price) FROM lab);'''
        self.cur.execute(string)
        row = self.cur.fetchone()
        return row

    def close_conn(self):
        self.conn.close()
