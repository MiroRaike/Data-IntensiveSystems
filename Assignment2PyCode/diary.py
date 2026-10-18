import tkinter as tk
import sqlite3
import style
import tkinter.messagebox

class diaryClass:
    def __init__(self, root, database_path):
        self.database_path = database_path
        self.root = root
        self.root.title("Diary")
        self.root.geometry("1000x800")

        self.var_date = tk.StringVar()
        self.var_descriptionOfDay = tk.StringVar()

        self.diaryEntries = []


        add_lbl = tk.Label(root, text="Add Diary Entry", font=("times new roman", 20, "bold"))

        date_lbl = tk.Label(root, text="Date", font=("times new roman", 15, "bold"))
        date_entry = tk.Entry(root, textvariable=self.var_date)

        descriptionOfDay_lbl = tk.Label(root, text="Description of Day", font=("times new roman", 15, "bold"))
        self.descriptionOfDay_entry = tk.Text(root, width=60, height=10)

        submit_btn = tk.Button(root, text="Submit", command=self.add,bg="green", fg="white", cursor="hand2", padx=100, pady=20)

                # ----------------- bill list -------------------
        date_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE)

        scrolly = tk.Scrollbar(date_frame, orient=tk.VERTICAL)
        self.Sales_List = tk.Listbox(
            date_frame, font=style.FONTGOUDYSMALL,
            bg=style.BGCOLORWHITE, yscrollcommand=scrolly.set
        )
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=tk.BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # --------------- bill area ----------------------
        bill_Frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE)

        lbl_title2 = tk.Label(
            bill_Frame, text="Diary Entry Area",
            font=("goudy old style", 20), bg="light blue"
        )
        #.pack(side=tk.TOP, fill=tk.X)

        delete_btn = tk.Button(self.root, text="Delete Entry", command=self.delete_entry, bg="red", fg="white", cursor="hand2", padx=100, pady=20)

        entry_lbl = tk.Label(root, text="Add Diary Entry", font=("times new roman", 20, "bold"))
        date_frame_label = tk.Label(root, text="Diary Entries", font=("times new roman", 20, "bold"))

        scrolly2 = tk.Scrollbar(bill_Frame, orient=tk.VERTICAL)
        self.bill_area = tk.Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=tk.RIGHT, fill=tk.Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=tk.BOTH, expand=1)

        add_lbl.grid(row=0, column=0,columnspan=2)
        date_lbl.grid(row=1, column=0)
        date_entry.grid(row=1, column=1)
        descriptionOfDay_lbl.grid(row=2, column=0)
        self.descriptionOfDay_entry.grid(row=2, column=1)
        submit_btn.grid(row=3, column=0, columnspan=2)
        entry_lbl.grid(row=4, column=0, columnspan=2)
        date_frame_label.grid(row=5, column=0)
        date_frame.grid(row=6, column=0)
        delete_btn.grid(row=7, column=0)
        bill_Frame.grid(row=6, column=1, rowspan=3)
        self.getAllDates()

    def add(self):
        con=sqlite3.connect(database=r''+self.database_path)
        cur=con.cursor()
        try:
            if self.var_date.get()=="":
               tkinter.messagebox.showerror("Error","Date must be required",parent=self.root)
            else:
                cur.execute("Select * from diary where date=?",(self.var_date.get(),))
                row=cur.fetchone()
                if row!=None:
                    tkinter.messagebox.showerror("Error","This date already assigned, try different",parent=self.root)
                else:
                    cur.execute("Insert into diary(date,description) values(?,?)",(
                        self.var_date.get(),
                        self.descriptionOfDay_entry.get('1.0',tk.END)
                    ))
                    con.commit()
                    tkinter.messagebox.showinfo("Success","Diary added successfully",parent=self.root)
                    self.clear()
        except Exception as ex:
            tk.messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def getAllDates(self):
        con=sqlite3.connect(database=r''+self.database_path)
        cur=con.cursor()
        try:
            cur.execute("Select date from diary")
            rows=cur.fetchall()
            if len(rows)!=0:
                for row in rows:
                    #print(row)
                    self.diaryEntries.append(row[0])
                    self.Sales_List.insert(tk.END,row[0])
        except Exception as ex:
            tkinter.messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self, ev):
        index = self.Sales_List.curselection()
        date = self.Sales_List.get(index)
        self.selected_date = date
        if not date:
            return

        con=sqlite3.connect(database=r''+self.database_path)
        cur=con.cursor()
        try:
            cur.execute("Select * from diary where date=?",(date,))
            row=cur.fetchone()
            if row!=None:
                self.clear()
                self.bill_area.insert(tk.END, row[2])
        except Exception as ex:
            tk.messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def delete_entry(self):
        #print(self.selected_date)
        con=sqlite3.connect(database=r''+self.database_path)
        cur=con.cursor()
        try:
            if self.selected_date=="":
                tkinter.messagebox.showerror("Error","Date must be required",parent=self.root)
            else:
                cur.execute("Select * from diary where date=?",(self.selected_date,))
                row=cur.fetchone()
                if row==None:
                    tkinter.messagebox.showerror("Error","This date is not assigned, try different",parent=self.root)
                else:
                    cur.execute("Delete from diary where date=?",( self.selected_date,))
                    con.commit()
                    tkinter.messagebox.showinfo("Success","Diary entry deleted successfully",parent=self.root)
                    self.clear()
        except Exception as ex:
            tk.messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        self.Sales_List.delete(0, tk.END)
        self.bill_area.delete('1.0', tk.END)
        self.diaryEntries.clear()
        self.getAllDates()

if __name__=="__main__":
    root=tk.Tk()
    obj=diaryClass(root, database_path="diary.db")
    root.mainloop()