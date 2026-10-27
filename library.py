import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

FILE_NAME = "library.txt"
books = {}


def load_books():
    global books

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                books = json.load(file)

            for book in books.values():
                book.setdefault("borrowed", 0)

        except (json.JSONDecodeError, OSError):
            books = {}
            messagebox.showwarning(
                "Warning",
                "Saved records could not be loaded."
            )


def save_books():
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(books, file, indent=4)
    except OSError:
        messagebox.showerror("Error", "Could not save the records.")


def refresh_books():
    for item in book_table.get_children():
        book_table.delete(item)

    for isbn, book in books.items():
        book_table.insert(
            "",
            "end",
            values=(
                book["title"],
                book["author"],
                isbn,
                book["quantity"],
                book["borrowed"]
            )
        )

    status.config(text=f"Total book records: {len(books)}")


def add_book():
    title = simpledialog.askstring(
        "Add Book", "Enter book title:", parent=root
    )
    if title is None:
        return

    author = simpledialog.askstring(
        "Add Book", "Enter author's name:", parent=root
    )
    if author is None:
        return

    isbn = simpledialog.askstring(
        "Add Book", "Enter ISBN:", parent=root
    )
    if isbn is None:
        return

    title = title.strip()
    author = author.strip()
    isbn = isbn.strip()

    if not title or not author or not isbn:
        messagebox.showerror(
            "Error", "All fields must be completed."
        )
        return

    if isbn in books:
        messagebox.showerror(
            "Error", "This ISBN already exists."
        )
        return

    quantity = simpledialog.askinteger(
        "Add Book",
        "Enter quantity available:",
        parent=root,
        minvalue=0
    )

    if quantity is None:
        return

    books[isbn] = {
        "title": title,
        "author": author,
        "quantity": quantity,
        "borrowed": 0
    }

    save_books()
    refresh_books()

    messagebox.showinfo(
        "Success", "Book added successfully."
    )


def search_book():
    query = simpledialog.askstring(
        "Search Book",
        "Enter title, author or ISBN:",
        parent=root
    )

    if query is None:
        return

    query = query.strip().lower()

    if not query:
        messagebox.showwarning(
            "Search", "Please enter a search term."
        )
        return

    results = []

    for isbn, book in books.items():
        if (
            query in book["title"].lower()
            or query in book["author"].lower()
            or query in isbn.lower()
        ):
            results.append(
                f'Title: {book["title"]}\n'
                f'Author: {book["author"]}\n'
                f'ISBN: {isbn}\n'
                f'Available: {book["quantity"]}\n'
                f'Borrowed: {book["borrowed"]}'
            )

    if results:
        messagebox.showinfo(
            "Search Results", "\n\n".join(results)
        )
    else:
        messagebox.showinfo(
            "Search Results", "No matching book found."
        )


def get_selected_book():
    selected = book_table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Book",
            "Select a book from the table first."
        )
        return None

    values = book_table.item(selected[0], "values")
    return values[2]


def borrow_book():
    isbn = get_selected_book()

    if isbn is None:
        return

    book = books[isbn]

    if book["quantity"] <= 0:
        messagebox.showwarning(
            "Unavailable",
            "No copies of this book are available."
        )
        return

    book["quantity"] -= 1
    book["borrowed"] += 1

    save_books()
    refresh_books()

    messagebox.showinfo(
        "Success", "Book borrowed successfully."
    )


def return_book():
    isbn = get_selected_book()

    if isbn is None:
        return

    book = books[isbn]

    if book["borrowed"] <= 0:
        messagebox.showwarning(
            "Return Book",
            "No borrowed copies are recorded for this book."
        )
        return

    book["quantity"] += 1
    book["borrowed"] -= 1

    save_books()
    refresh_books()

    messagebox.showinfo(
        "Success", "Book returned successfully."
    )


def low_stock():
    results = []

    for isbn, book in books.items():
        if book["quantity"] < 3:
            results.append(
                f'{book["title"]} - '
                f'{book["quantity"]} copies available '
                f'(ISBN: {isbn})'
            )

    if results:
        messagebox.showinfo(
            "Low Stock", "\n".join(results)
        )
    else:
        messagebox.showinfo(
            "Low Stock", "No low-stock books found."
        )


def close_program():
    save_books()
    root.destroy()


root = tk.Tk()
root.title("City Central Library")
root.geometry("900x520")
root.minsize(750, 420)

load_books()

heading = ttk.Label(
    root,
    text="CITY CENTRAL LIBRARY",
    font=("Arial", 18, "bold")
)
heading.pack(pady=(15, 5))

subtitle = ttk.Label(
    root,
    text="Book Inventory and Borrowing System"
)
subtitle.pack(pady=(0, 12))

button_frame = ttk.Frame(root)
button_frame.pack(pady=5)

ttk.Button(
    button_frame, text="Add Book",
    command=add_book
).grid(row=0, column=0, padx=4, pady=5)

ttk.Button(
    button_frame, text="Search Book",
    command=search_book
).grid(row=0, column=1, padx=4, pady=5)

ttk.Button(
    button_frame, text="Borrow Selected",
    command=borrow_book
).grid(row=0, column=2, padx=4, pady=5)

ttk.Button(
    button_frame, text="Return Selected",
    command=return_book
).grid(row=0, column=3, padx=4, pady=5)

ttk.Button(
    button_frame, text="Low Stock",
    command=low_stock
).grid(row=0, column=4, padx=4, pady=5)

ttk.Button(
    button_frame, text="Refresh",
    command=refresh_books
).grid(row=0, column=5, padx=4, pady=5)

columns = (
    "title", "author", "isbn", "quantity", "borrowed"
)

table_frame = ttk.Frame(root, padding=10)
table_frame.pack(fill="both", expand=True)

book_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

book_table.heading("title", text="Book Title")
book_table.heading("author", text="Author")
book_table.heading("isbn", text="ISBN")
book_table.heading("quantity", text="Available")
book_table.heading("borrowed", text="Borrowed")

book_table.column("title", width=230)
book_table.column("author", width=180)
book_table.column("isbn", width=170)
book_table.column("quantity", width=100, anchor="center")
book_table.column("borrowed", width=100, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=book_table.yview
)

book_table.configure(
    yscrollcommand=scrollbar.set
)

book_table.pack(
    side="left", fill="both", expand=True
)
scrollbar.pack(side="right", fill="y")

status = ttk.Label(
    root, text="", anchor="w", padding=10
)
status.pack(fill="x")

root.protocol("WM_DELETE_WINDOW", close_program)

refresh_books()

root.mainloop()