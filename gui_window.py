from tkinter import *

window = Tk()
window.geometry("350x200")
window.title("SANIA")

def clicked():
    lbl.configure(text="Button was clicked")
btn = Button(window, text="Click me", command=clicked)
btn.grid(column=1, row=0)

lbl = Label(window, text="Hello")
lbl.grid(column=2, row=0)

window.mainloop()