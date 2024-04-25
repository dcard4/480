import tkinter as tk
from tkinter import messagebox, Tk, Entry, Label, Button, Toplevel, Frame
import psycopg2
import librarian

def create_connection():
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="project",
            user="postgres",
            password="Ariana1904",
            port="5432")
        return conn
    except psycopg2.DatabaseError as e:
        messagebox.showerror("Database Connection Error", e)
        return None


def exit_application(root):
    """ Handle the clean exit of the application. """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        
        
def open_librarian_window(root):
    """ Open the librarian window and setup initial UI controls. """
    root.withdraw()  
    librarian_window = tk.Toplevel(root)
    librarian_window.title("Librarian Dashboard")
    librarian_window.geometry("600x400")

    tk.Label(librarian_window, text="Welcome, Librarian!", font=("Arial", 18)).pack(pady=20)

    
    tk.Button(librarian_window, text="Add Book", command=lambda: add_book(librarian_window)).pack(pady=10)
    
    
    tk.Button(librarian_window, text="Add Magazine", command=lambda: add_magazine(librarian_window)).pack(pady=10)


    tk.Button(librarian_window, text="Add Journal", command=lambda: add_journal(librarian_window)).pack(pady=10)
    

    tk.Button(librarian_window, text="Edit Document", command=lambda: edit_document_interface(librarian_window)).pack(pady=5)

    
    tk.Button(librarian_window, text="Remove Document", command=lambda: delete_document_interface(librarian_window)).pack(pady=20)
    
    
    tk.Button(librarian_window, text="Edit Client", command=lambda: edit_client(librarian_window)).pack(pady=20)
    
    
    tk.Button(librarian_window, text="Logout", command=lambda: logout(librarian_window, root)).pack(pady=20)

    return librarian_window


def insert_book(isbn, title, authors, edition, pages, barcode=None):
    """Insert a new book into the database if the ISBN does not already exist."""
    conn = create_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        cur.execute("SELECT isbn FROM Book WHERE isbn = %s", (isbn,))
        if cur.fetchone():
            messagebox.showerror("Error", "ISBN already exists in the database. Cannot add duplicate book.")
            return

        
        if barcode:
            cur.execute("SELECT barcode FROM Documents WHERE barcode = %s", (barcode,))
            if not cur.fetchone():
                cur.execute("INSERT INTO Documents (barcode, copies, publisher, year) VALUES (%s, 1, 'Unknown', 2021)", (barcode,))
            cur.execute("INSERT INTO NonJournal (isbn, barcode) VALUES (%s, %s)", (isbn, barcode))

        
        cur.execute(
            "INSERT INTO Book (isbn, title, authors, edition, pages) VALUES (%s, %s, %s, %s, %s)",
            (isbn, title, authors, edition, pages))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Failed to add book: {str(e)}")
    finally:
        if conn:
            conn.close()


def add_book(librarian_window):
    """Creates and displays the form for adding a new book in a separate window."""
    book_window = Toplevel(librarian_window)
    book_window.title("Add New Book")
    book_window.geometry("400x500")

    book_frame = Frame(book_window)
    book_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    
    entries = {}

    
    field_labels = ['ISBN', 'Title', 'Authors', 'Edition', 'Pages', 'Barcode number']
    for field in field_labels:
        Label(book_frame, text=f"{field}:").pack()
        entry = Entry(book_frame)
        entry.pack()
        entries[field.lower()] = entry

    
    Button(book_frame, text="Submit Book", command=lambda: insert_book(
        entries['isbn'].get(),
        entries['title'].get(),
        entries['authors'].get(),
        entries['edition'].get(),
        entries['pages'].get(),
        entries['barcode number'].get() or None  
    )).pack(pady=10)


def insert_magazine(isbn, name, month, barcode=None):
    """Insert a new magazine into the database, ensuring all foreign key constraints are met."""
    conn = create_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        # Check if the ISBN already exists in NonJournal
        cur.execute("SELECT isbn FROM NonJournal WHERE isbn = %s", (isbn,))
        if not cur.fetchone():
            # If not, check if barcode is provided or not
            if barcode:
                # Check if the barcode exists in Documents
                cur.execute("SELECT barcode FROM Documents WHERE barcode = %s", (barcode,))
                if not cur.fetchone():  # If barcode does not exist, add it
                    cur.execute("INSERT INTO Documents (barcode, copies, publisher, year) VALUES (%s, 1, 'Unknown Publisher', 2021)", (barcode,))
                cur.execute("INSERT INTO NonJournal (isbn, barcode) VALUES (%s, %s)", (isbn, barcode))
            else:
                messagebox.showerror("Error", "Barcode is required for new ISBN entries.")
                return

        # Now safe to insert into Magazine
        cur.execute(
            "INSERT INTO Magazine (isbn, name, month) VALUES (%s, %s, %s)",
            (isbn, name, month))
        conn.commit()
        messagebox.showinfo("Success", "Magazine added successfully")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Failed to add magazine: {str(e)}")
    finally:
        if conn:
            conn.close()


def add_magazine(librarian_window):
    """Creates and displays the form for adding a new magazine in a separate window."""
    magazine_window = Toplevel(librarian_window)
    magazine_window.title("Add New Magazine")
    magazine_window.geometry("400x300")

    magazine_frame = Frame(magazine_window)
    magazine_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    
    entries = {}

   
    field_labels = ['ISBN', 'Name', 'Month', 'Barcode Number']
    for field in field_labels:
        Label(magazine_frame, text=f"{field}:").pack()
        entry = Entry(magazine_frame)
        entry.pack()
        entries[field.lower()] = entry

    
    Button(magazine_frame, text="Submit Magazine", command=lambda: insert_magazine(
        entries['isbn'].get(),
        entries['name'].get(),
        entries['month'].get(),
        entries['barcode number'].get() or None  
    )).pack(pady=10)


def insert_journal(title, issue, name, authors, number, barcode):
    """Insert a new journal into the database, ensuring all foreign key constraints are met."""
    conn = create_connection()  # Assuming you have a function to handle database connections
    if conn is None:
        return

    try:
        cur = conn.cursor()
        # Check and insert into Documents if needed
        cur.execute("SELECT barcode FROM Documents WHERE barcode = %s", (barcode,))
        if not cur.fetchone():
            cur.execute("INSERT INTO Documents (barcode, copies, publisher, year) VALUES (%s, 0, %s, 2021)", (barcode, name))

        # Insert into Journal
        cur.execute(
            "INSERT INTO Journal (title, issue, name, authors, number, barcode) VALUES (%s, %s, %s, %s, %s, %s)",
            (title, issue, name, authors, number, barcode))
        conn.commit()
        messagebox.showinfo("Success", "Journal added successfully")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Failed to add journal: {str(e)}")
    finally:
        if conn:
            conn.close()
            
            
def add_journal(librarian_window):
    """Creates and displays the form for adding a new journal in a separate window."""
    journal_window = Toplevel(librarian_window)
    journal_window.title("Add New Journal")
    journal_window.geometry("400x500")

    journal_frame = Frame(journal_window)
    journal_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Dictionary to hold the entry widgets, mapped by field name
    entries = {}

    # List of labels corresponding to the Journal fields
    field_labels = ['Title', 'Issue', 'Name', 'Authors', 'Number', 'Barcode']
    for field in field_labels:
        Label(journal_frame, text=f"{field}:").pack()
        entry = Entry(journal_frame)
        entry.pack()
        entries[field.lower()] = entry

    # Button to submit the new journal details
    Button(journal_frame, text="Submit Journal", command=lambda: insert_journal(
        entries['title'].get(),
        entries['issue'].get(),
        entries['name'].get(),
        entries['authors'].get(),
        entries['number'].get(),
        entries['barcode'].get()
    )).pack(pady=10)            


def edit_document_interface(librarian_window):
    """Creates and displays the form for fetching and editing an existing document."""
    edit_window = Toplevel(librarian_window)
    edit_window.title("Edit Document")
    edit_window.geometry("400x300")

    edit_frame = Frame(edit_window)
    edit_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Entry to input ISBN for fetching the document
    Label(edit_frame, text="ISBN:").pack()
    isbn_entry = Entry(edit_frame)
    isbn_entry.pack()

    # Button to fetch the document details
    Button(edit_frame, text="Fetch Document", command=lambda: fetch_document_details(isbn_entry.get(), edit_window)).pack(pady=10)


def fetch_document_details(isbn, parent_window):
    """Fetches and displays the document details for editing."""
    conn = create_connection()  # Assuming you have a function to handle database connections
    if conn is None:
        return

    try:
        cur = conn.cursor()
        # Assume the document information is in the Book table for simplicity
        cur.execute("SELECT title, authors, edition, pages FROM Book WHERE isbn = %s", (isbn,))
        data = cur.fetchone()
        if data:
            show_edit_form(data, isbn, parent_window)
        else:
            messagebox.showerror("Error", "No document found with that ISBN.")
    except psycopg2.DatabaseError as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            conn.close()


def show_edit_form(data, isbn, parent_window):
    """Shows the form to edit document details."""
    title, authors, edition, pages = data
    edit_frame = Frame(parent_window)
    edit_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Create and pack entry widgets for editing document details
    entries = {}
    labels = ['Title', 'Authors', 'Edition', 'Pages']
    current_values = [title, authors, edition, pages]
    for label, value in zip(labels, current_values):
        Label(edit_frame, text=f"{label}:").pack()
        entry = Entry(edit_frame)
        entry.insert(0, value)  # Pre-fill the entry with current value
        entry.pack()
        entries[label.lower()] = entry

    # Button to submit the updated details
    Button(edit_frame, text="Update Document", command=lambda: update_document(isbn, entries, parent_window)).pack(pady=10)


def update_document(isbn, entries, parent_window):
    """Updates the document details in the database."""
    title = entries['title'].get()
    authors = entries['authors'].get()
    edition = entries['edition'].get()
    pages = entries['pages'].get()

    conn = create_connection()  # Assuming you have a function to handle database connections
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("UPDATE Book SET title = %s, authors = %s, edition = %s, pages = %s WHERE isbn = %s",
                    (title, authors, edition, pages, isbn))
        conn.commit()
        messagebox.showinfo("Success", "Document updated successfully")
        parent_window.destroy()  # Close the edit window upon successful update
    except psycopg2.DatabaseError as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Failed to update document: {str(e)}")
    finally:
        if conn:
            conn.close()


def delete_document_interface(librarian_window):
    
    delete_window = Toplevel(librarian_window)
    delete_window.title("Delete Document")
    delete_window.geometry("300x200")

    delete_frame = Frame(delete_window)
    delete_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    
    Label(delete_frame, text="Enter ISBN to Delete:").pack()
    isbn_entry = Entry(delete_frame)
    isbn_entry.pack(pady=10)

    
    Button(delete_frame, text="Delete Document", command=lambda: confirm_deletion(isbn_entry.get(), delete_window)).pack()


def confirm_deletion(isbn, parent_window):
    
    if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this document?"):
        delete_document_by_isbn(isbn)
        parent_window.destroy()
    else:
        messagebox.showinfo("Cancellation", "Deletion cancelled.")


def delete_document_by_isbn(isbn):
    
    conn = create_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        cur.execute("DELETE FROM Book WHERE isbn = %s", (isbn,))
        # Follow similar steps for Magazine and NonJournal if applicable
        conn.commit()
        messagebox.showinfo("Success", "Document deleted successfully")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Failed to delete document: {str(e)}")
    finally:
        if conn:
            conn.close()


def edit_client(librarian_window):
    """Creates and displays the form for fetching and editing an existing document."""
    edit_window = Toplevel(librarian_window)
    edit_window.title("Edit Client Info")
    edit_window.geometry("400x300")

    edit_frame = Frame(edit_window)
    edit_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    
    Label(edit_frame, text="email:").pack()
    email_entry = Entry(edit_frame)
    email_entry.pack()

    # Button to fetch the document details
    Button(edit_frame, text="Fetch Client", command=lambda: fetch_client_details(email_entry.get(), edit_window)).pack(pady=10)


def fetch_client_details(email, parent_window):
    
    conn = create_connection()  
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        cur.execute("SELECT name, email FROM Clients WHERE email = %s", (email,))
        data = cur.fetchone()
        if data:
            show_edit_form(data, email, parent_window)
        else:
            messagebox.showerror("Error", "No Client found with that email.")
    except psycopg2.DatabaseError as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            conn.close()


def show_client_edit_form(client, parent_window):
    """Shows the form to edit client details."""
    name, email = client
    edit_form = Frame(parent_window)
    edit_form.pack(pady=20, fill=tk.BOTH, expand=True)

    # Create and pack entry widgets for editing client details
    name_entry = Entry(edit_form)
    name_entry.insert(0, name)
    name_entry.pack()

    # Button to submit the updated details
    Button(edit_form, text="Update Client", command=lambda: update_client(email, name_entry.get())).pack(pady=10)

def update_client(email, new_name):
    """Updates the client details in the database."""
    conn = create_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("UPDATE Clients SET name = %s WHERE email = %s", (new_name, email))
        conn.commit()
        messagebox.showinfo("Success", "Client updated successfully")
    except psycopg2.DatabaseError as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Failed to update client: {str(e)}")
    finally:
        if conn:
            conn.close()
    
def logout(librarian_window, root):
    """ Logout from the librarian window and show the main login window. """
    librarian_window.destroy()
    root.deiconify()


def main(root):
    """ Main function to start the librarian module independently, if needed. """
    open_librarian_window(root)
    root.mainloop()