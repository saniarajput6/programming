from tkinter import *
import tkinter.font as tkfont
from tkinter.ttk import Combobox


window = Tk()
window.geometry("600x350")
window.title("GUI")


default_font = tkfont.nametofont("TkDefaultFont")


default_font.configure(size=12, family="Arial")


lbl0 = Label(window, text="GUI", font=("Arial Bold", 20))
lbl0.grid(column=0, row=0, sticky="W")

name_lbl = Label(window, text="Full Name:", font=("Arial Bold", 12))
name_lbl.grid(column=0, row=1, sticky="W")

name_input_txt = Entry(window, width=30, font=("Arial", 12))
name_input_txt.grid(column=0, row=2, sticky="W", padx=5, pady=5)

age_lbl = Label(window, text="Age:", font=("Arial Bold", 12))
age_lbl.grid(column=0, row=3, sticky="W")

age_input_txt = Entry(window, width=30, font=("Arial", 12))
age_input_txt.grid(column=0, row=4, sticky="W", padx=5, pady=5)

gender_lbl = Label(window, text="Gender:", font=("Arial Bold", 12))
gender_lbl.grid(column=0, row=5, sticky="W")

selected = IntVar()
selected.set(1)

rad0 = Radiobutton(window, text="Male", value=0, variable=selected)
rad0.grid(column=0, row=6, sticky="w")
rad1 = Radiobutton(window, text="Female", value=1, variable=selected)
rad1.grid(column=0, row=7, sticky="w")

course_lbl = Label(window, text="Course:", font=("Arial Bold", 12))
course_lbl.grid(column=0, row=8, sticky="W")

combo = Combobox(window)
combo["values"] = ["BTEC IT", "BTEC Business", "ACCA", "ICDL"]
combo.current(1)
combo.grid(column=0, row=9, sticky="W", padx=5, pady=5)

email_lbl = Label(window, text="Email:", font=("Arial Bold", 12))
email_lbl.grid(column=0, row=10, sticky="W")

email_input_txt = Entry(window, width=30, font=("Arial", 12))
email_input_txt.grid(column=0, row=11, sticky="W", padx=5, pady=5)

chk_state = BooleanVar()
chk_state.set(False)

chk = Checkbutton(window, text="Confirmation?", var=chk_state)
chk.grid(column=0, row=12, sticky="W")

def submit():
    if name_input_txt.get() == "" or age_input_txt.get() == "" or email_input_txt.get() == "" or not chk_state.get():
        lbl_submit.configure(text="Please fill in all the boxes!")
    else:
        lbl_submit.configure(text="Submitted!")


btn_submit = Button(window, text="Submit", command=submit)
btn_submit.grid(column=0, row=13, sticky="W")

lbl_submit = Label(window, text="Submit")
lbl_submit.grid(column=0, row=14, sticky="W")

def clear():
    lbl_clear.configure(text="Cleared!")
    name_input_txt.delete(0, END)
    age_input_txt.delete(0, END)
    email_input_txt.delete(0, END)
    checkbox = chk_state.set(False)
    lbl_submit.configure(text="Submit")

btn_clear = Button(window, text="Clear", command=clear)
btn_clear.grid(column=2, row=13, sticky="W")

lbl_clear = Label(window, text="Clear")
lbl_clear.grid(column=2, row=14, sticky="W")


window.mainloop()
