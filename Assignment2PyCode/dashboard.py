# Reporposed some code from software maintenance courses final project
import tkinter as tk
import sqlite3

from diary import diaryClass
from passwordmanager import passwordClass
from create_databases import create_databases

class dashboardClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("400x600")

        tk.Label(root, text="Dashboard", font=("Arial", 24)).pack(pady=20)
        tk.Button(root, text="Diary Miro", command=self.diary, padx=100, pady=20).pack(side="top", pady=10)
        tk.Button(root, text="Password Manager", command=self.password_manager, padx=100, pady=20).pack(side="top", pady=10)
        tk.Button(root, text="Diary Anon", command=self.anon_diary, padx=100, pady=20).pack(side="top", pady=10)
        tk.Button(root, text="Make tables", command=create_databases, padx=100, pady=20).pack(side="top", pady=10)
        tk.Button(root, text="Fill tables", command=self.fill_tables, padx=100, pady=20).pack(side="top", pady=10)
        tk.Button(root, text="Exit", command=root.quit, padx=100, pady=20).pack(side="top", pady=10)

    def diary(self):
        self.new_win = tk.Toplevel(self.root)
        self.app = diaryClass(self.new_win, database_path="diary.db")  # Pass the database path to the diaryClass

    def password_manager(self):
        self.new_win = tk.Toplevel(self.root)
        self.app = passwordClass(self.new_win)

    def anon_diary(self):
        self.new_win = tk.Toplevel(self.root)
        self.app = diaryClass(self.new_win, database_path="anon_diary.db")  # Pass the database path to the diaryClass
    
    def fill_tables(self):
        # Fill the tables with sample data
        con = sqlite3.connect(database=r'diary.db')
        cur = con.cursor()
        cur.execute("INSERT INTO diary (date, description) VALUES (?, ?)", ("2024-01-01", "Sample diary entry"))
        con.commit()
        cur.execute("INSERT INTO diary (date, description) VALUES (?, ?)", ("2024-01-02", "Sample diary entry2"))
        con.commit()
        cur.execute("INSERT INTO diary (date, description) VALUES (?, ?)", ("2024-01-03", "Sample diary entry3"))
        con.commit()
        con.close()

        con = sqlite3.connect(database=r'anon_diary.db')
        cur = con.cursor()
        cur.execute("INSERT INTO diary (date, description) VALUES (?, ?)", ("2024-01-01", "Sample anonymous diary entry"))
        con.commit()
        cur.execute("INSERT INTO diary (date, description) VALUES (?, ?)", ("2024-01-02", "Sample anonymous diary entry2"))
        con.commit()
        cur.execute("INSERT INTO diary (date, description) VALUES (?, ?)", ("2024-01-03", "Sample anonymous diary entry3"))
        con.commit()
        con.close()

        con = sqlite3.connect(database=r'password.db')
        cur = con.cursor()
        cur.execute("INSERT INTO passwords (url, username, password) VALUES (?, ?, ?)", ("https://example.com", "user1", "pass1"))
        con.commit()
        cur.execute("INSERT INTO passwords (url, username, password) VALUES (?, ?, ?)", ("https://example2.com", "user2", "pass2"))
        con.commit()
        cur.execute("INSERT INTO passwords (url, username, password) VALUES (?, ?, ?)", ("https://example3.com", "user3", "pass3"))
        con.commit()
        con.close()

if __name__ == "__main__":
    root = tk.Tk()
    obj = dashboardClass(root)
    root.mainloop()
