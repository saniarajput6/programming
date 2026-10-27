from struct import pack
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

FILE_NAME = "library.txt"
BACKUP_FILE = "library_backup.txt"
HISTORY_FILE = "library_history.txt"

books = {}

def load_books():
    global books

    if not os.path.exists(FILE_NAME):
        books = {}
        return

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            saved_books = json.load(file)

        if not isinstance(saved_books, dict):
            raise ValueError("The saved records are not in the correct format.")

        for isbn, book in saved_books.items():
            if not isinstance(book, dict):
                raise ValueError("A book record is invalid.")

            if not all(key in book for key in ("title", "author", "quantity")):
                raise ValueError("A book record is missing information.")

            if not isinstance(book["quantity"], int) or book["quantity"] < 0:
                raise ValueError("A book has an invalid quantity.")

            book.setdefault("borrowed", 0)

            if not isinstance(book["borrowed"], int) or book["borrowed"] < 0:
                raise ValueError("A book has an invalid borrowed count.")

            if book["quantity"] + book["borrowed"] < 0:
                raise ValueError("A book record has an invalid quantity.")

        books = saved_books

    except (json.JSONDecodeError, OSError, ValueError) as error:
        books = {}
        messagebox.showwarning(
            "Loading Error",
            f"The saved records could not be loaded.\n\n{error}")
        
def save_books():
    try:
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                previous_data = file.read()

            with open(BACKUP_FILE, "w", encoding="utf-8") as file:
                file.write(previous_data)

        temporary_file = FILE_NAME + ".tmp"

        with open(temporary_file, "w", encoding="utf-8") as file:
            json.dump(books, file, indent=4)

        os.replace(temporary_file, FILE_NAME)
        return True

    except (OSError, TypeError) as error:
        messagebox.showerror(
            "Save Error",
            f"The records could not be saved.\n\n{error}")
        
        return False

def record_history(action, isbn, title):
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    entry = {
        "date": date_time,
        "action": action,
        "isbn": isbn,
        "title": title}
    
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(entry) + "\n")
    except OSError:
        messagebox.showwarning(
            "History Error",
            "The action was completed, but the history could not be saved.")
        
def load_history():
    history = []

    if not os.path.exists(HISTORY_FILE):
        return history

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    entry = json.loads(line)

                    if isinstance(entry, dict):
                        history.append(entry)

                except json.JSONDecodeError:
                    continue

    except OSError:
        messagebox.showerror(
            "History Error",
            "The borrowing history could not be opened.")

    return history

def refresh_books():
    for item in book_table.get_children():
        book_table.delete(item)

    search_text = search_entry.get().strip().lower()

    for isbn, book in sorted(
        books.items(),
        key=lambda item: item[1]["title"].lower()):
    
        title = book["title"]
        author = book["author"]

        if search_text:
            if (
                search_text not in title.lower()
                and search_text not in author.lower()
                and search_text not in isbn.lower()):
            
                continue

        book_table.insert(
            "",
            "end",
            iid=isbn,
            values=(
                title,
                author,
                isbn,
                book["quantity"],
                book["borrowed"]))
            
    status_label.config(
        text=f"Total books: {len(books)} | "
             f"Copies available: {sum(b['quantity'] for b in books.values())}")
    
def clear_search():
    search_entry.delete(0, tk.END)
    refresh_books()

def get_selected_isbn():
    selected = book_table.selection()

    if not selected:
        messagebox.showwarning(
            "Select a Book",
            "Please select a book from the table first.")
        
        return None

    return selected[0]

def add_book():
    title = simpledialog.askstring(
        "Add Book",
        "Enter the book title:",
        parent=root)
    
    if title is None:
        return

    author = simpledialog.askstring(
        "Add Book",
        "Enter the author's name:",
        parent=root)

    if author is None:
        return

    isbn = simpledialog.askstring(
        "Add Book",
        "Enter the ISBN:",
        parent=root)

    if isbn is None:
        return

    title = title.strip()
    author = author.strip()
    isbn = isbn.strip()

    if not title or not author or not isbn:
        messagebox.showerror(
            "Missing Information",
            "Please complete all the fields.")
        
        return

    if any(char.isspace() for char in isbn):
        messagebox.showerror(
            "Invalid ISBN",
            "The ISBN must not contain spaces.")
        
        return

    if isbn in books:
        messagebox.showerror(
            "Duplicate ISBN",
            "A book with this ISBN already exists.")
        
        return

    quantity = simpledialog.askinteger(
        "Add Book",
        "Enter the number of copies available:",
        parent=root,
        minvalue=0,
        maxvalue=100000)
    
    if quantity is None:
        return

    books[isbn] = {
        "title": title,
        "author": author,
        "quantity": quantity,
        "borrowed": 0}

    if save_books():
        record_history("Book added", isbn, title)
        refresh_books()

        messagebox.showinfo(
            "Success",
            f'"{title}" was added successfully.')
        
    else:
        del books[isbn]

def edit_book():
    isbn = get_selected_isbn()

    if isbn is None:
        return

    book = books[isbn]

    title = simpledialog.askstring(
        "Edit Book",
        "Enter the book title:",
        initialvalue=book["title"],
        parent=root)
    
    if title is None:
        return

    author = simpledialog.askstring(
        "Edit Book",
        "Enter the author's name:",
        initialvalue=book["author"],
        parent=root)
    
    if author is None:
        return

    title = title.strip()
    author = author.strip()

    if not title or not author:
        messagebox.showerror(
            "Invalid Information",
            "Title and author cannot be empty.")
        
        return

    old_title = book["title"]
    old_author = book["author"]

    book["title"] = title
    book["author"] = author

    if save_books():
        record_history("Book details edited", isbn, title)
        refresh_books()
        messagebox.showinfo(
            "Success",
            "Book details updated successfully.")
        
    else:
        book["title"] = old_title
        book["author"] = old_author

def delete_book():
    isbn = get_selected_isbn()

    if isbn is None:
        return

    book = books[isbn]

    if book["borrowed"] > 0:
        messagebox.showwarning(
            "Cannot Delete",
            "This book has borrowed copies recorded. "
            "Return those copies before deleting the record.")
        
        return

    answer = messagebox.askyesno(
        "Delete Book",
        f'Are you sure you want to delete "{book["title"]}"?')

    if not answer:
        return

    removed_book = books.pop(isbn)

    if save_books():
        record_history("Book deleted", isbn, removed_book["title"])
        refresh_books()
        messagebox.showinfo(
            "Success",
            "Book record deleted successfully.")
        
    else:
        books[isbn] = removed_book
        refresh_books()

def search_book():
    query = simpledialog.askstring(
        "Search Book",
        "Enter a title, author or ISBN:",
        parent=root)
    
    if query is None:
        return

    query = query.strip()

    if not query:
        messagebox.showwarning(
            "Search",
            "Please enter something to search for.")
        return

    search_entry.delete(0, tk.END)
    search_entry.insert(0, query)
    refresh_books()

    if not book_table.get_children():
        messagebox.showinfo(
            "Search Results",
            "No matching books were found.")

def borrow_book():
    isbn = get_selected_isbn()

    if isbn is None:
        return

    book = books[isbn]

    if book["quantity"] <= 0:
        messagebox.showwarning(
            "Book Unavailable",
            "There are no copies available to borrow.")
        
        return

    book["quantity"] -= 1
    book["borrowed"] += 1

    if save_books():
        record_history("Book borrowed", isbn, book["title"])
        refresh_books()

        messagebox.showinfo(
            "Success",
            f'"{book["title"]}" has been borrowed.')
        
    else:
        book["quantity"] += 1
        book["borrowed"] -= 1
        refresh_books()

def return_book():
    isbn = get_selected_isbn()

    if isbn is None:
        return

    book = books[isbn]

    if book["borrowed"] <= 0:
        messagebox.showwarning(
            "Return Book",
            "No borrowed copies are recorded for this book.")
        
        return

    book["quantity"] += 1
    book["borrowed"] -= 1

    if save_books():
        record_history("Book returned", isbn, book["title"])
        refresh_books()

        messagebox.showinfo(
            "Success",
            f'"{book["title"]}" has been returned.')
        
    else:
        book["quantity"] -= 1
        book["borrowed"] += 1
        refresh_books()

def low_stock():
    results = []

    for isbn, book in books.items():
        if book["quantity"] < 3:
            results.append(
                f'Title: {book["title"]}\n'
                f'ISBN: {isbn}\n'
                f'Available copies: {book["quantity"]}')

    if results:
        messagebox.showinfo(
            "Low-Stock Books",
            "\n\n".join(results))
        
    else:
        messagebox.showinfo(
            "Low-Stock Books",
            "There are no low-stock books.")

def show_history():
    history = load_history()

    if not history:
        messagebox.showinfo(
            "Library History",
            "No library activity has been recorded yet.")
        
        return

    history_window = tk.Toplevel(root)
    history_window.title("Library Activity History")
    history_window.geometry("750x400")
    history_window.transient(root)

    heading = ttk.Label(
        history_window,
        text="LIBRARY ACTIVITY HISTORY",
        font=("Arial", 14, "bold"))
    
    heading.pack(pady=12)

    columns = ("date", "action", "title", "isbn")

    history_table = ttk.Treeview(
        history_window,
        columns=columns,
        show="headings")
    
    history_table.heading("date", text="Date and Time")
    history_table.heading("action", text="Action")
    history_table.heading("title", text="Book Title")
    history_table.heading("isbn", text="ISBN")

    history_table.column("date", width=150)
    history_table.column("action", width=140)
    history_table.column("title", width=250)
    history_table.column("isbn", width=150)

    scrollbar = ttk.Scrollbar(
        history_window,
        orient="vertical",
        command=history_table.yview)

    history_table.configure(
        yscrollcommand=scrollbar.set)

    history_table.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=(0, 10))

    scrollbar.pack(
        side="right",
        fill="y",
        padx=(0, 10),
        pady=(0, 10))

    for entry in reversed(history):
        history_table.insert(
            "",
            "end",
            values=(
                entry.get("date", ""),
                entry.get("action", ""),
                entry.get("title", ""),
                entry.get("isbn", "")))

def show_about():
    messagebox.showinfo(
        "About the Library System",
        "City Central Library\n\n"
        "This application helps staff manage book records.\n\n"
        "Features include adding, editing, deleting, searching, "
        "borrowing and returning books, checking low stock, "
        "and viewing activity history.\n\n"
        "Book records are stored in a local file.")

root = tk.Tk()
root.title("City Central Library - Book Management")
root.geometry("1050x600")
root.minsize(850, 500)

load_books()

heading = ttk.Label(
    root,
    text="CITY CENTRAL LIBRARY",
    font=("Arial", 20, "bold"))

heading.pack(pady=(15, 4))

subtitle = ttk.Label(
    root,
    text="Book Inventory and Borrowing System")

subtitle.pack(pady=(0, 12))

search_frame = ttk.Frame(root, padding=(10, 5))
search_frame.pack(fill="x")

ttk.Label(
    search_frame,
    text="Search:"
).pack(side="left", padx=(0, 6))

search_entry = ttk.Entry(search_frame, width=35)
search_entry.pack(side="left", padx=4)
search_entry.bind(
    "<KeyRelease>",
    lambda event: refresh_books())

ttk.Button(
    search_frame,
    text="Clear Search",
    command=clear_search
).pack(side="left", padx=5)

button_frame = ttk.Frame(root, padding=8)
button_frame.pack(fill="x")

buttons = [
    ("Add Book", add_book),
    ("Edit Book", edit_book),
    ("Delete Book", delete_book),
    ("Search Book", search_book),
    ("Borrow Selected", borrow_book),
    ("Return Selected", return_book),
    ("Low Stock", low_stock),
    ("History", show_history),
    ("Refresh", refresh_books),
    ("About", show_about)]

for number, (text, command) in enumerate(buttons):
    ttk.Button(
        button_frame,
        text=text,
        command=command
    ).grid(
        row=number // 5,
        column=number % 5,
        padx=4,
        pady=4,
        sticky="ew")

for column in range(5):
    button_frame.columnconfigure(column, weight=1)

table_frame = ttk.Frame(root, padding=(10, 5, 10, 8))
table_frame.pack(fill="both", expand=True)

columns = ("title", "author", "isbn", "quantity", "borrowed")

book_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse")

book_table.heading("title", text="Book Title")
book_table.heading("author", text="Author")
book_table.heading("isbn", text="ISBN")
book_table.heading("quantity", text="Available")
book_table.heading("borrowed", text="Borrowed")

book_table.column("title", width=260, minwidth=150)
book_table.column("author", width=200, minwidth=120)
book_table.column("isbn", width=180, minwidth=130)
book_table.column("quantity", width=100, anchor="center")
book_table.column("borrowed", width=100, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=book_table.yview)

book_table.configure(
    yscrollcommand=scrollbar.set)

book_table.pack(
    side="left",
    fill="both",
    expand=True)

scrollbar.pack(side="right", fill="y")

status_label = ttk.Label(
    root,
    text="",
    anchor="w",
    padding=(12, 8))

status_label.pack(fill="x")

def close_program():
    if messagebox.askyesno(
        "Exit",
        "Do you want to close the library system?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", close_program)

refresh_books()
root.mainloop()