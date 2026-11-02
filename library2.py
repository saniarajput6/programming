import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

FILE_NAME = "library.txt"
BACKUP_FILE = "library_backup.txt"
HISTORY_FILE = "library_history.txt"

books = {}


# LOAD AND SAVE RECORDS

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
            f"The saved records could not be loaded.\n\n{error}"
        )


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
            f"The records could not be saved.\n\n{error}"
        )
        return False


def record_history(action, isbn, title):
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    entry = {
        "date": date_time,
        "action": action,
        "isbn": isbn,
        "title": title
    }

    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(entry) + "\n")
    except OSError:
        messagebox.showwarning(
            "History Error",
            "The action was completed, but the history could not be saved."
        )


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
            "The borrowing history could not be opened."
        )

    return history


# DISPLAY BOOKS

def refresh_books():
    for item in book_table.get_children():
        book_table.delete(item)

    search_text = search_entry.get().strip().lower()

    for isbn, book in sorted(
        books.items(),
        key=lambda item: item[1]["title"].lower()
    ):
        title = book["title"]
        author = book["author"]

        if search_text:
            if (
                search_text not in title.lower()
                and search_text not in author.lower()
                and search_text not in isbn.lower()
            ):
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
                book["borrowed"]
            )
        )

    status_label.config(
        text=f"Total books: {len(books)} | "
             f"Copies available: {sum(b['quantity'] for b in books.values())}"
    )


def clear_search():
    search_entry.delete(0, tk.END)
    refresh_books()


def get_selected_isbn():
    selected = book_table.selection()

    if not selected:
        messagebox.showwarning(
            "Select a Book",
            "Please select a book from the table first."
        )
        return None

    return selected[0]


# ADD A BOOK

def add_book():
    title = simpledialog.askstring(
        "Add Book",
        "Enter the book title:",
        parent=root
    )

    if title is None:
        return

    author = simpledialog.askstring(
        "Add Book",
        "Enter the author's name:",
        parent=root
    )

    if author is None:
        return

    isbn = simpledialog.askstring(
        "Add Book",
        "Enter the ISBN:",
        parent=root
    )

    if isbn is None:
        return

    title = title.strip()
    author = author.strip()
    isbn = isbn.strip()

    if not title or not author or not isbn:
        messagebox.showerror(
            "Missing Information",
            "Please complete all the fields."
        )
        return

    if any(char.isspace() for char in isbn):
        messagebox.showerror(
            "Invalid ISBN",
            "The ISBN must not contain spaces."
        )
        return

    if isbn in books:
        messagebox.showerror(
            "Duplicate ISBN",
            "A book with this ISBN already exists."
        )
        return

    quantity = simpledialog.askinteger(
        "Add Book",
        "Enter the number of copies available:",
        parent=root,
        minvalue=0,
        maxvalue=100000
    )

    if quantity is None:
        return

    books[isbn] = {
        "title": title,
        "author": author,
        "quantity": quantity,
        "borrowed": 0
    }

    if save_books():
        record_history("Book added", isbn, title)
        refresh_books()

        messagebox.showinfo(
            "Success",
            f'"{title}" was added successfully.'
        )
    else:
        del books[isbn]


# EDIT A BOOK

def edit_book():
    isbn = get_selected_isbn()

    if isbn is None:
        return

    book = books[isbn]

    title = simpledialog.askstring(
        "Edit Book",
        "Enter the book title:",
        initialvalue=book["title"],
        parent=root
    )

    if title is None:
        return

    author = simpledialog.askstring(
        "Edit Book",
        "Enter the author's name:",
        initialvalue=book["author"],
        parent=root
    )

    if author is None:
        return

    title = title.strip()
    author = author.strip()

    if not title or not author:
        messagebox.showerror(
            "Invalid Information",
            "Title and author cannot be empty."
        )
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
            "Book details updated successfully."
        )
    else:
        book["title"] = old_title
        book["author"] = old_author


# DELETE A BOOK

def delete_book():
    isbn = get_selected_isbn()

    if isbn is None:
        return

    book = books[isbn]

    if book["borrowed"] > 0:
        messagebox.showwarning(
            "Cannot Delete",
            "This book has borrowed copies recorded. "
            "Return those copies before deleting the record."
        )
        return

    answer = messagebox.askyesno(
        "Delete Book",
        f'Are you sure you want to delete "{book["title"]}"?'
    )

    if not answer:
        return

    removed_book = books.pop(isbn)

    if save_books():
        record_history("Book deleted", isbn, removed_book["title"])
        refresh_books()
        messagebox.showinfo(
            "Success",
            "Book record deleted successfully."
        )
    else:
        books[isbn] = removed_book
        refresh_books()


# SEARCH FOR BOOKS

def search_book():
    query = simpledialog.askstring(
        "Search Book",
        "Enter a title, author or ISBN:",
        parent=root
    )

    if query is None:
        return

    query = query.strip()

    if not query:
        messagebox.showwarning(
            "Search",
            "Please enter something to search for."
        )
        return

    search_entry.delete(0, tk.END)
    search_entry.insert(0, query)
    refresh_books()

    if not book_table.get_children():
        messagebox.showinfo(
            "Search Results",
            "No matching books were found."
        )


# BORROW A BOOK

def borrow_book():
    isbn = get_selected_isbn()

    if isbn is None:
        return

    book = books[isbn]

    if book["quantity"] <= 0:
        messagebox.showwarning(
            "Book Unavailable",
            "There are no copies available to borrow."
        )
        return

    book["quantity"] -= 1
    book["borrowed"] += 1

    if save_books():
        record_history("Book borrowed", isbn, book["title"])
        refresh_books()

        messagebox.showinfo(
            "Success",
            f'"{book["title"]}" has been borrowed.'
        )
    else:
        book["quantity"] += 1
        book["borrowed"] -= 1
        refresh_books()


# RETURN A BOOK

def return_book():
    isbn = get_selected_isbn()

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

    if save_books():
        record_history("Book returned", isbn, book["title"])
        refresh_books()

        messagebox.showinfo(
            "Success",
            f'"{book["title"]}" has been returned.'
        )
    else:
        book["quantity"] -= 1
        book["borrowed"] += 1
        refresh_books()


# LOW-STOCK REPORT

def low_stock():
    results = []

    for isbn, book in books.items():
        if book["quantity"] < 3:
            results.append(
                f'Title: {book["title"]}\n'
                f'ISBN: {isbn}\n'
                f'Available copies: {book["quantity"]}'
            )

    if results:
        messagebox.showinfo(
            "Low-Stock Books",
            "\n\n".join(results)
        )
    else:
        messagebox.showinfo(
            "Low-Stock Books",
            "There are no low-stock books."
        )


# BORROWING AND RETURNING HISTORY

def show_history():
    history = load_history()

    if not history:
        messagebox.showinfo(
            "Library History",
            "No library activity has been recorded yet."
        )
        return

    history_window = tk.Toplevel(root)
    history_window.title("Library Activity History")
    history_window.geometry("750x400")
    history_window.transient(root)

    heading = ttk.Label(
        history_window,
        text="LIBRARY ACTIVITY HISTORY",
        font=("Arial", 14, "bold")
    )
    heading.pack(pady=12)

    columns = ("date", "action", "title", "isbn")

    history_table = ttk.Treeview(
        history_window,
        columns=columns,
        show="headings"
    )

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
        command=history_table.yview
    )

    history_table.configure(
        yscrollcommand=scrollbar.set
    )

    history_table.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=(0, 10)
    )

    scrollbar.pack(
        side="right",
        fill="y",
        padx=(0, 10),
        pady=(0, 10)
    )

    for entry in reversed(history):
        history_table.insert(
            "",
            "end",
            values=(
                entry.get("date", ""),
                entry.get("action", ""),
                entry.get("title", ""),
                entry.get("isbn", "")
            )
        )


# ABOUT THE PROGRAM

def show_about():
    messagebox.showinfo(
        "About the Library System",
        "City Central Library\n\n"
        "This application helps staff manage book records.\n\n"
        "Features include adding, editing, deleting, searching, "
        "borrowing and returning books, checking low stock, "
        "and viewing activity history.\n\n"
        "Book records are stored in a local file."
    )


# MAIN WINDOW

root = tk.Tk()
root.title("City Central Library - Book Management")
root.geometry("1050x600")
root.minsize(850, 500)
root.configure(bg="#F8F3E9")
# root.resizable(width=False, height=False)

# Appearance settings: a polished, warm library theme.
style = ttk.Style()
style.theme_use("clam")

BACKGROUND = "#F3F0E8"
PANEL = "#FAF8F2"
DARK_GREEN = "#294B3D"
MID_GREEN = "#496B58"
LIGHT_GREEN = "#E2EADF"
GOLD = "#C69B55"
TEXT = "#34443A"

root.configure(bg=BACKGROUND)

style.configure("TFrame", background=BACKGROUND)
style.configure("TLabel", background=BACKGROUND, foreground=TEXT,
                font=("Arial", 10))
style.configure(
    "TButton",
    background=LIGHT_GREEN,
    foreground=DARK_GREEN,
    font=("Arial", 9, "bold"),
    padding=(10, 8),
    borderwidth=0
)
style.map(
    "TButton",
    background=[("active", "#D0DDCE"), ("pressed", "#BECFBC")],
    foreground=[("active", DARK_GREEN)]
)
style.configure(
    "TEntry",
    fieldbackground=PANEL,
    foreground=TEXT,
    padding=7,
    borderwidth=1,
    relief="flat"
)
style.configure(
    "Treeview",
    background=PANEL,
    fieldbackground=PANEL,
    foreground=TEXT,
    rowheight=31,
    borderwidth=0,
    font=("Arial", 10)
)
style.configure(
    "Treeview.Heading",
    background=DARK_GREEN,
    foreground="#FFFFFF",
    font=("Arial", 9, "bold"),
    padding=(8, 10),
    relief="flat"
)
style.map(
    "Treeview",
    background=[("selected", "#D9C79F")],
    foreground=[("selected", DARK_GREEN)]
)
style.map(
    "Treeview.Heading",
    background=[("active", MID_GREEN)]
)

load_books()

# Clean library banner with a small bookshelf illustration.
header = tk.Canvas(
    root,
    height=112,
    bg=BACKGROUND,
    highlightthickness=0
)
header.pack(fill="x")

# Main banner
header.create_rectangle(0, 0, 1080, 105, fill=DARK_GREEN, outline="")
header.create_rectangle(0, 100, 1080, 105, fill=GOLD, outline="")

header.create_text(
    55, 35,
    text="CITY CENTRAL LIBRARY",
    anchor="w",
    fill="#FFFFFF",
    font=("Arial", 21, "bold")
)
header.create_text(
    57, 66,
    text="BOOK INVENTORY  •  BORROWING  •  RETURNS",
    anchor="w",
    fill="#E5E9DF",
    font=("Arial", 9, "bold")
)

# Simple decorative bookshelf on the right, kept separate from the text.
header.create_rectangle(790, 78, 1080, 85, fill="#C69B55", outline="")
spine_colours = ["#D9A16F", "#9DB7A0", "#D8C28D", "#A9B8C9", "#C88F86", "#D6B27A"]
book_x = 812
for index, colour in enumerate(spine_colours):
    book_height = [39, 47, 34, 43, 38, 46][index]
    book_width = 23
    header.create_rectangle(
        book_x, 78 - book_height, book_x + book_width, 78,
        fill=colour, outline="#F3EBDD", width=1
    )
    header.create_line(
        book_x + 5, 78 - book_height + 7,
        book_x + 5, 72,
        fill="#F3EBDD", width=1
    )
    book_x += 27

header.create_text(
    1008, 52,
    text="READ\nMORE",
    fill="#E5D4B2",
    font=("Arial", 8, "bold"),
    justify="center"
)

# SEARCH BAR

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
    lambda event: refresh_books()
)

ttk.Button(
    search_frame,
    text="Clear Search",
    command=clear_search
).pack(side="left", padx=5)


# BUTTONS

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
    ("About", show_about)
]

button_colours = [
    "#DCE7DA", "#DCE7DA", "#EAD9D1", "#DCE7DA", "#D7E3E0",
    "#D7E3E0", "#E9E0C9", "#DCE7DA", "#DCE7DA", "#E9E0C9"
]

for number, (text, command) in enumerate(buttons):
    button_style = f"Library{number}.TButton"
    style.configure(
        button_style,
        background=button_colours[number],
        foreground=DARK_GREEN,
        font=("Arial", 9, "bold"),
        padding=(8, 6),
        borderwidth=0
    )
    style.map(
        button_style,
        background=[("active", "#C8D8C5"), ("pressed", "#B7CBB5")]
    )
    ttk.Button(
        button_frame,
        text=text,
        command=command,
        style=button_style
    ).grid(
        row=number // 5,
        column=number % 5,
        padx=4,
        pady=4,
        sticky="ew"
    )

for column in range(5):
    button_frame.columnconfigure(column, weight=1)


# BOOK TABLE

table_frame = ttk.Frame(root, padding=(10, 5, 10, 8))
table_frame.pack(fill="both", expand=True)

columns = (
    "title",
    "author",
    "isbn",
    "quantity",
    "borrowed"
)

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

book_table.column("title", width=260, minwidth=150)
book_table.column("author", width=200, minwidth=120)
book_table.column("isbn", width=180, minwidth=130)
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
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# STATUS BAR

status_label = ttk.Label(
    root,
    text="",
    anchor="w",
    padding=(12, 10),
    font=("Arial", 9, "bold"),
    background="#E5E9DF",
    foreground=DARK_GREEN
)
status_label.pack(fill="x")


# CLOSE THE PROGRAM

def close_program():
    if messagebox.askyesno(
        "Exit",
        "Do you want to close the library system?"
    ):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", close_program)

refresh_books()

root.mainloop()