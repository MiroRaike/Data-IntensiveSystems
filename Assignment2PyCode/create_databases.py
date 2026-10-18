import sqlite3

class create_databases:
    def __init__(self):
        self.create_anon_diary_db()
        self.create_password_db()
        self.create_diary_db()

    def create_anon_diary_db(self):
        con=sqlite3.connect(database=r'anon_diary.db')
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS diary(id INTEGER PRIMARY KEY AUTOINCREMENT,date text,description text)")
        con.commit()

    def create_password_db(self):
        con=sqlite3.connect(database=r'password.db')
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS passwords(eid INTEGER PRIMARY KEY AUTOINCREMENT,url text,username text,password text)")
        con.commit()

    def create_diary_db(self):
        con=sqlite3.connect(database=r'diary.db')
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS diary(id INTEGER PRIMARY KEY AUTOINCREMENT,date text,description text)")
        con.commit()
