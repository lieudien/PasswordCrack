#!/usr/bin/python

from Tkinter import *
import PasswordCracking
SEPARATOR = '*'*75
typeList = [ "md5", "sha1", "sha256", "sha512"]

master = Tk()

# Function section
def make_WindoW(title, Width, height):
    master.title(title)
    master.geometry("{}x{}".format(Width,height))

def get_selection():
    selection = str(var.get())
    return selection

def run():
    PasswordCracking.main()

# GUI section
make_WindoW("Crack4Beginner", 400, 600)

# INPUT HEADER
Label(master, text=SEPARATOR).pack(fill='x')
Label(master, text="INPUT", font="Helvetica 12 bold").pack(fill='x')
Label(master, text=SEPARATOR).pack(fill='x')

# PassWord field
Label(master, text="Password").pack(anchor=W)
pWd_entry = Entry(master, text="Enter a passWord")
pWd_entry.pack(anchor=W)

# Hash algorithm selection
Label(master, text="Hash algorithm type").pack(anchor=W)
radioList = []
var = IntVar()
for i in range(len(typeList)):
    radioList.append(Radiobutton(master, text=typeList[i], variable=var, value=i+1, command=get_selection))
    radioList[i].pack(anchor=W)
var.set(1)

# Panel contains 2 buttons for Run and Quit
panel_bottom = PanedWindow(master, orient=HORIZONTAL)
panel_bottom.pack(fill=BOTH, expand=1, side=BOTTOM)

run_button = Button(master, text="Run", command=run)
panel_bottom.add(run_button, stretch='always')

quit_button = Button(master, text="Quit", command=master.quit)
panel_bottom.add(quit_button, stretch='always')

# Panel for information
scrollbar = Scrollbar(master)
scrollbar.pack(side=RIGHT, fill='y')

listbox = Listbox(master, bg='grey', yscrollcommand=scrollbar.set, height='300')
listbox.insert(END, "The end...")
listbox.pack(fill=BOTH)

# Make the WindoW visible
master.mainloop()
