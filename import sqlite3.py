import psycopg2
import tkinter as tk
from tkinter import messagebox

def create_connection():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="your_library",
            user="postgre",
            password="test",
            port="5450")
        return conn
    except psycopg2.DatabaseError as e:
        messagebox.showerror("Database Connection Error", e)
        return None

def add_client(conn, email, password, name):
    """Add a new client into the Clients table"""
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Clients(email, name, password) VALUES (%s, %s, %s)", (email, name, password))
        conn.commit()
        cur.close()
        messagebox.showinfo("Registration", "Registration successful")
    except psycopg2.IntegrityError:
        messagebox.showerror("Registration Error", "Email already registered")
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))

def check_login(conn, email, password):
    """Check login credentials"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT password FROM Clients WHERE email = %s", (email,))
        result = cur.fetchone()
        cur.close()
        if result and result[0] == password:
            messagebox.showinfo("Login", "Login successful")
        else:
            messagebox.showerror("Login Error", "Invalid email or password")
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))

def search_document(conn, barcode):
    """Search for a document by barcode"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Documents WHERE barcode = %s", (barcode,))
        result = cur.fetchone()
        cur.close()
        if result:
            messagebox.showinfo("Search Result", f"Document Found: {result}")
        else:
            messagebox.showerror("Search Error", "Document not found")
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))

def register():
    email = entry_email.get()
    password = entry_password.get()
    name = entry_name.get()
    if email and password and name:
        conn = create_connection()
        if conn:
            add_client(conn, email, password, name)
            conn.close()
    else:
        messagebox.showerror("Registration Error", "All fields are required")

def login():
    email = entry_email.get()
    password = entry_password.get()
    if email and password:
        conn = create_connection()
        if conn:
            check_login(conn, email, password)
            conn.close()
    else:
        messagebox.showerror("Login Error", "Both email and password are required")

def search():
    barcode = entry_barcode.get()
    if barcode:
        conn = create_connection()
        if conn:
            search_document(conn, barcode)
            conn.close()
    else:
        messagebox.showerror("Search Error", "Barcode is required")

# GUI setup
root = tk.Tk()
root.title("Library System")

# Registration and Login
tk.Label(root, text="Email:").grid(row=0, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=0, column=1)

tk.Label(root, text="Password:").grid(row=1, column=0)
entry_password = tk.Entry(root, show='*')
entry_password.grid(row=1, column=1)

tk.Label(root, text="Name (for registration only):").grid(row=2, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=2, column=1)

tk.Button(root, text="Register", command=register).grid(row=3, column=0)
tk.Button(root, text="Login", command=login).grid(row=3, column=1)

# Document Search
tk.Label(root, text="Search Document Barcode:").grid(row=4, column=0)
entry_barcode = tk.Entry(root)
entry_barcode.grid(row=4, column=1)
tk.Button(root, text="Search", command=search).grid(row=5, column=0, columnspan=2)

root.mainloop()
