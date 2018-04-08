#!/usr/bin/python

from Tkinter import *

master = Tk()

width = 400
height = 300

master.title("Crack4Beginner")
master.geometry("{}x{}".format(width, height))

Label(master, text="INPUT", font="Helvetica 12 bold").grid(row=0)

run_button = Button(master, text="Run")
run_button.grid(row=4, column=0, sticky=N+S+E)

quit_button = Button(master, text="Quit", command=master.quit)
quit_button.grid(row=4, column=2, sticky=N+S+W)

master.mainloop()