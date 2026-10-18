import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Database configurations with schemas and dummy data
DB_CONFIGS = {
    'inventory': {
        'name': 'Inventory Database',
        'file': 'inventory.db',
        'table': 'items',
        'fields': [
            {'name': 'name', 'label': 'Item Name'},
            {'name': 'category', 'label': 'Category'},
            {'name': 'quantity', 'label': 'Quantity'},
            {'name': 'price', 'label': 'Price ($)'}
        ],
        'dummy_data': [
            ('Laptop Pro 15', 'Electronics', '12', '1299.99'),
            ('Ergonomic Chair', 'Furniture', '25', '249.50'),
            ('Wireless Mouse', 'Accessories', '50', '29.99'),
            ('Standing Desk', 'Furniture', '8', '499.00')
        ]
    },
    'employees': {
        'name': 'Employees Database',
        'file': 'employees.db',
        'table': 'staff',
        'fields': [
            {'name': 'name', 'label': 'Full Name'},
            {'name': 'role', 'label': 'Job Role'},
            {'name': 'department', 'label': 'Department'},
            {'name': 'email', 'label': 'Email'}
        ],
        'dummy_data': [
            ('Alice Johnson', 'Software Engineer', 'Engineering', 'alice@company.com'),
            ('Bob Smith', 'Product Manager', 'Product', 'bob@company.com'),
            ('Charlie Davis', 'UX Designer', 'Design', 'charlie@company.com'),
            ('Diana Prince', 'HR Specialist', 'Human Resources', 'diana@company.com')
        ]
    },
    'projects': {
        'name': 'Projects Database',
        'file': 'projects.db',
        'table': 'tasks',
        'fields': [
            {'name': 'title', 'label': 'Project Title'},
            {'name': 'status', 'label': 'Status'},
            {'name': 'priority', 'label': 'Priority'},
            {'name': 'due_date', 'label': 'Due Date'}
        ],
        'dummy_data': [
            ('Website Redesign', 'In Progress', 'High', '2026-06-30'),
            ('Database Migration', 'Pending', 'Medium', '2026-07-15'),
            ('Security Audit', 'Completed', 'High', '2026-05-01'),
            ('Mobile App Beta', 'In Progress', 'Low', '2026-08-10')
        ]
    }
}

class MultiDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Multi-Database Manager")
        self.root.geometry("1000x600")
        self.root.minsize(850, 500)

        # Initialize databases and load dummy data
        self.init_databases()

        # Current active database key
        self.current_db_key = tk.StringVar(value='inventory')
        self.current_db_key.trace('w', lambda *args: self.load_database_view())

        # Selected record ID for updating/deleting
        self.selected_record_id = None

        self.create_widgets()
        self.load_database_view()

    def init_databases(self):
        """Creates database files and populates them if empty."""
        for db_key, config in DB_CONFIGS.items():
            conn = sqlite3.connect(config['file'])
            cursor = conn.cursor()
            
            fields_sql = ", ".join([f"{f['name']} TEXT" for f in config['fields']])
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {config['table']} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {fields_sql}
                )
            ''')
            
            cursor.execute(f"SELECT COUNT(*) FROM {config['table']}")
            if cursor.fetchone()[0] == 0:
                placeholders = ", ".join(["?" for _ in config['fields']])
                field_names = ", ".join([f['name'] for f in config['fields']])
                cursor.executemany(f'''
                    INSERT INTO {config['table']} ({field_names})
                    VALUES ({placeholders})
                ''', config['dummy_data'])
                
            conn.commit()
            conn.close()

    def create_widgets(self):
        # Top Frame: Database Selection Navigation
        top_frame = ttk.LabelFrame(self.root, text=" Select Database ", padding=10)
        top_frame.pack(fill="x", padx=10, pady=10)

        for db_key, config in DB_CONFIGS.items():
            rb = ttk.Radiobutton(
                top_frame, 
                text=config['name'], 
                value=db_key, 
                variable=self.current_db_key
            )
            rb.pack(side="left", padx=20)

        # Main Container (Split into Table View (Left) and Form Control (Right))
        main_container = ttk.PanedWindow(self.root, orient="horizontal")
        main_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Left Pane: Table and Records Display
        left_frame = ttk.Frame(main_container, padding=5)
        main_container.add(left_frame, weight=3)

        self.tree_frame = ttk.Frame(left_frame)
        self.tree_frame.pack(fill="both", expand=True)

        # Right Pane: CRUD Form Controls
        self.right_frame = ttk.LabelFrame(main_container, text=" Record Details ", padding=15)
        main_container.add(right_frame := self.right_frame, weight=2)

        # Form fields container (dynamically built per DB)
        self.form_container = ttk.Frame(right_frame)
        self.form_container.pack(fill="x", expand=True)

        # Action Buttons Frame
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill="x", pady=15)

        self.btn_add = ttk.Button(btn_frame, text="Add New", command=self.add_record)
        self.btn_add.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_update = ttk.Button(btn_frame, text="Update Selected", command=self.update_record, state="disabled")
        self.btn_update.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_delete = ttk.Button(btn_frame, text="Delete Selected", command=self.delete_record, state="disabled")
        self.btn_delete.pack(side="left", expand=True, fill="x", padx=2)

        btn_clear = ttk.Button(btn_frame, text="Clear", command=self.clear_form)
        btn_clear.pack(side="left", expand=True, fill="x", padx=2)

    def load_database_view(self):
        """Switches active database interface, redraws table and form fields."""
        db_key = self.current_db_key.get()
        config = DB_CONFIGS[db_key]

        # Clear selection state
        self.selected_record_id = None
        self.btn_update.config(state="disabled")
        self.btn_delete.config(state="disabled")

        # Recreate Treeview table
        for widget in self.tree_frame.winfo_children():
            widget.destroy()

        columns = ['id'] + [f['name'] for f in config['fields']]
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('id', text='ID')
        self.tree.column('id', width=40, anchor='center')

        for field in config['fields']:
            self.tree.heading(field['name'], text=field['label'])
            self.tree.column(field['name'], width=120, anchor='w')

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind('<<TreeviewSelect>>', self.on_row_select)

        # Recreate Form Entry Fields
        for widget in self.form_container.winfo_children():
            widget.destroy()

        self.entry_vars = {}
        for field in config['fields']:
            lbl = ttk.Label(self.form_container, text=field['label'])
            lbl.pack(anchor="w", pady=(5, 2))
            
            var = tk.StringVar()
            entry = ttk.Entry(self.form_container, textvariable=var, font=("Arial", 10))
            entry.pack(fill="x", pady=(0, 5))
            self.entry_vars[field['name']] = var

        self.refresh_table_data()

    def refresh_table_data(self):
        """Fetches records from SQLite database and populates the treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        db_key = self.current_db_key.get()
        config = DB_CONFIGS[db_key]

        conn = sqlite3.connect(config['file'])
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {config['table']}")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert('', 'end', values=row)

    def on_row_select(self, event):
        """Populates form fields when a table row is clicked."""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item_data = self.tree.item(selected_items[0])['values']
        if not item_data:
            return

        self.selected_record_id = item_data[0]
        db_key = self.current_db_key.get()
        config = DB_CONFIGS[db_key]

        # Populate entry fields (skip ID at index 0)
        for idx, field in enumerate(config['fields']):
            self.entry_vars[field['name']].set(item_data[idx + 1])

        self.btn_update.config(state="normal")
        self.btn_delete.config(state="normal")

    def clear_form(self):
        """Resets form fields and clears selection."""
        self.selected_record_id = None
        for var in self.entry_vars.values():
            var.set("")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.btn_update.config(state="disabled")
        self.btn_delete.config(state="disabled")

    def add_record(self):
        """Inserts a new record into the current active database."""
        db_key = self.current_db_key.get()
        config = DB_CONFIGS[db_key]

        values = [var.get().strip() for var in self.entry_vars.values()]
        if any(v == "" for v in values):
            messagebox.showerror("Error", "All fields must be filled out to add a record.")
            return

        placeholders = ", ".join(["?" for _ in config['fields']])
        field_names = ", ".join([f['name'] for f in config['fields']])

        conn = sqlite3.connect(config['file'])
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {config['table']} ({field_names}) VALUES ({placeholders})", values)
        conn.commit()
        conn.close()

        self.refresh_table_data()
        self.clear_form()
        messagebox.showinfo("Success", "Record added successfully!")

    def update_record(self):
        """Updates the selected record in the current active database."""
        if not self.selected_record_id:
            return

        db_key = self.current_db_key.get()
        config = DB_CONFIGS[db_key]

        values = [var.get().strip() for var in self.entry_vars.values()]
        if any(v == "" for v in values):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        set_clause = ", ".join([f"{f['name']} = ?" for f in config['fields']])
        query_values = values + [self.selected_record_id]

        conn = sqlite3.connect(config['file'])
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {config['table']} SET {set_clause} WHERE id = ?", query_values)
        conn.commit()
        conn.close()

        self.refresh_table_data()
        self.clear_form()
        messagebox.showinfo("Success", "Record updated successfully!")

    def delete_record(self):
        """Deletes the selected record from the current active database."""
        if not self.selected_record_id:
            return

        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            return

        db_key = self.current_db_key.get()
        config = DB_CONFIGS[db_key]

        conn = sqlite3.connect(config['file'])
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {config['table']} WHERE id = ?", (self.selected_record_id,))
        conn.commit()
        conn.close()

        self.refresh_table_data()
        self.clear_form()
        messagebox.showinfo("Success", "Record deleted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiDBApp(root)
    root.mainloop()