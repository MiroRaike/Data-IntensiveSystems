import tkinter as tk
import sqlite3
import style
import tkinter.messagebox

class passwordClass:
    def __init__(self, root):
        self.root = root
        self.root.title("password")
        self.root.geometry("850x550")

        #self.var_date = tk.StringVar()
        self.var_site = tk.StringVar()
        self.var_username = tk.StringVar()
        self.var_password = tk.StringVar()
        self.url_string = tk.StringVar()
        self.password_string = tk.StringVar()

        self.passwordEntries = []


        add_lbl = tk.Label(root, text="Add password Entry", font=("times new roman", 20, "bold"))

        site_lbl = tk.Label(root, text="Site/URL", font=("times new roman", 15, "bold"))
        site_entry = tk.Entry(root, textvariable=self.var_site, width=50,)

        username_lbl = tk.Label(root, text="Username", font=("times new roman", 15, "bold"))
        username_entry = tk.Entry(root, textvariable=self.var_username, width=50)

        password_lbl = tk.Label(root, text="Password", font=("times new roman", 15, "bold"))
        password_entry = tk.Entry(root, textvariable=self.var_password, width=50)

        submit_btn = tk.Button(root, text="Submit", command=self.add,bg="green", fg="white", cursor="hand2", padx=100, pady=20)

        manager_lbl = tk.Label(root, text="Password Manager", font=("times new roman", 20, "bold"))

        #.pack(side=tk.TOP, fill=tk.X)

        delete_btn = tk.Button(self.root, text="Delete Entry", command=self.delete_entry, bg="red", fg="white", cursor="hand2", padx=100, pady=20)

        date_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE)
        date_frame_label = tk.Label(root, text="Diary Entries", font=("times new roman", 20, "bold"))

        scrolly = tk.Scrollbar(date_frame, orient=tk.VERTICAL)
        self.Passwords_List = tk.Listbox(
            date_frame, font=style.FONTGOUDYSMALL,
            bg=style.BGCOLORWHITE, yscrollcommand=scrolly.set
        )

        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        scrolly.config(command=self.Passwords_List.yview)
        self.Passwords_List.pack(fill=tk.BOTH, expand=1)
        self.Passwords_List.bind("<ButtonRelease-1>", self.get_data)

        url_ent = tk.Entry(root,textvariable=self.url_string,fg="black",bg="white",bd=0,state="readonly")
        db_url_frame1 = tk.Label(self.root, bd=3, relief=tk.RIDGE, text="Username Area", font=("times new roman", 15, "bold"), padx=2)

        ent = tk.Entry(root,textvariable=self.password_string,fg="black",bg="white",bd=0,state="readonly")
        db_password_frame1 = tk.Label(self.root, bd=3, relief=tk.RIDGE, text="Password Area", font=("times new roman", 15, "bold"), padx=2)


        add_lbl.grid(row=0, column=0,columnspan=2)
        site_lbl.grid(row=1, column=0)
        site_entry.grid(row=1, column=1)
        username_lbl.grid(row=2, column=0)
        username_entry.grid(row=2, column=1)
        password_lbl.grid(row=3, column=0)
        password_entry.grid(row=3, column=1)
        submit_btn.grid(row=1, column=2, rowspan=3)

        manager_lbl.grid(row=4, column=0, columnspan=2)
        date_frame_label.grid(row=5, column=0)
        date_frame.grid(row=6, column=0, rowspan=2)
        delete_btn.grid(row=8, column=0)
        db_url_frame1.grid(row=6, column=1)
        url_ent.grid(row=6, column=2, sticky="nsew")
        db_password_frame1.grid(row=7, column=1)
        ent.grid(row=7, column=2, sticky="nsew")
        #password_frame.grid(row=6, column=1, rowspan=2)

        self.getAllDates()

    def add(self):
        con=sqlite3.connect(database=r'password.db')
        cur=con.cursor()
        try:
            if self.var_site.get()=="":
               tkinter.messagebox.showerror("Error","Site must be required",parent=self.root)
            else:
                cur.execute("Select * from passwords where url=?",(self.var_site.get(),))
                row=cur.fetchone()
                if row!=None:
                    tkinter.messagebox.showerror("Error","This site already assigned, try different",parent=self.root)
                else:
                    cur.execute("Insert into passwords(url,username,password) values(?,?,?)",(
                        self.var_site.get(),
                        self.var_username.get(),
                        self.var_password.get()
                    ))
                    con.commit()
                    tkinter.messagebox.showinfo("Success","Password added successfully",parent=self.root)
                    self.clear()
        except Exception as ex:
            tk.messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def getAllDates(self):
        con=sqlite3.connect(database=r'password.db')
        cur=con.cursor()
        try:
            cur.execute("Select url from passwords")
            rows=cur.fetchall()
            if len(rows)!=0:
                for row in rows:
                    self.passwordEntries.append(row[0])
                    self.Passwords_List.insert(tk.END,row[0])
        except Exception as ex:
            tkinter.messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self, ev):
        index = self.Passwords_List.curselection()
        date = self.Passwords_List.get(index)
        self.selected_date = date
        if not date:
            return

        con=sqlite3.connect(database=r'password.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from passwords where url=?",(date,))
            row=cur.fetchone()
            if row!=None:
                self.clear()
                self.url_string.set(row[2])
                self.password_string.set(row[3])
        except Exception as ex:
            tk.messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def delete_entry(self):
        con=sqlite3.connect(database=r'password.db')
        cur=con.cursor()
        try:
            if self.selected_date=="":
                tkinter.messagebox.showerror("Error","url must be required",parent=self.root)
            else:
                cur.execute("Select * from passwords where url=?",(self.selected_date,))
                row=cur.fetchone()
                if row==None:
                    tkinter.messagebox.showerror("Error","This url is not assigned, try different",parent=self.root)
                else:
                    cur.execute("Delete from passwords where url=?",( self.selected_date,))
                    con.commit()
                    tkinter.messagebox.showinfo("Success","password entry deleted successfully",parent=self.root)
                    self.clear()
        except Exception as ex:
            tk.messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        self.Passwords_List.delete(0, tk.END)
        self.url_string.set("")
        self.password_string.set("")
        self.passwordEntries.clear()
        self.getAllDates()

if __name__=="__main__":
    root=tk.Tk()
    obj=passwordClass(root)
    root.mainloop()