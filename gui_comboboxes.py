from tkinter import *
window = Tk()
window.geometry("350x200")
window.title("SANIA")
selected = IntVar()
selected.set(1)
rad0 = Radiobutton(window, text="Zero", value=0, variable=selected)
rad0.grid(column=0, row=0)
rad1 = Radiobutton(window, text="One", value=1, variable=selected)
rad1.grid(column=1, row=0)
rad2 = Radiobutton(window, text="Two", value=2, variable=selected)
rad2.grid(column=2, row=0)

def clicked():
    res = f"You have selected {selected.get()}"
    output.set(res)

btn = Button(window, text="Click Me", command=clicked)
btn.grid(column=1, row=0)

output = StringVar()

txt = Entry(window, width=30, textvariable=output, state="readonly")
txt.grid(column=2, row=0)

window.mainloop()
