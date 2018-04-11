#!/usr/bin/python

from Tkinter import *
import multiprocessing
import sys
import time
import getpass
from passlib.hash import md5_crypt as pwd_context

SEPARATOR = '*'*75
typeList = [ "md5", "sha1", "sha256", "sha512"]

master = Tk()
listbox = Listbox(master, bg='grey', yscrollcommand=scrollbar.set, height='300')
PASSWORD_FILE = "common-passwords.txt"

def printGUI(message):
    listbox.insert(END, message)

class Worker(multiprocessing.Process):
    def __init__(self, id, queue, pwd_hash, pwd_list):
        multiprocessing.Process.__init__(self)
        self.id = id
        self.queue = queue
        self.pwd_hash = pwd_hash
        self.pwd_list = pwd_list

    def run(self):
        proc_id = self.id
        printGUI("Creating process %d" % self.id)
        try:
            num_procs = multiprocessing.cpu_count() * 2
            for i in self.pwd_list:
                if (not self.queue.empty()):
                    check = self.queue.get()
                    if (check is None):
                        printGUI("[Process %d: Exiting...]\n" % proc_id)
                        return

                if (pwd_context.verify(i, self.pwd_hash)):
                    print("[Process %d: Found: %s]\n" % (proc_id, i))
                    [self.queue.put(None) for j in range(num_procs - 1)]
                    return
        except KeyboardInterrupt:
            print ("[Process %d : Shutdown by KeyboardInterrupt.]\n" % self.id)
            pass

def encrypt(password, type):
    pwd_hash = pwd_context.hash(password.strip())
    print("Your hash: {}".format(pwd_hash))
    return pwd_hash

def printTime(start_time):
    end = time.time() - start_time
    if (end > 60):
        printGUI("Time executed: {:.2f} minutes".format(end/60))
    else:
        printGUI("Time executed: {} seconds".format(end))

def main():
    processes = []
    # Establish communication queue
    queue = multiprocessing.Queue()

    # Get user input
    usr_input = getpass.getpass("Enter a password:")
    pwd_hash = encrypt(usr_input, None)

    # Start worker processes
    num_procs = multiprocessing.cpu_count() * 2

    # Load the password list
    with open(PASSWORD_FILE, 'rb') as file:
        pwd_list = [i.strip() for i in file]
    size = len(pwd_list) / num_procs
    size = int(round(size, -1))

    for i in range(num_procs):
        lists = pwd_list[i*size: (i+1)*size]
        processes.append(Worker(i, queue, pwd_hash, lists))
        print("[Process %d has %d words]" % (i, len(lists)))

    start_time = time.time()
    [p.start() for p in processes]

    for w in processes:
        w.join()

    printTime(start_time)

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

listbox.insert(END, "The end...")
listbox.pack(fill=BOTH)

# Make the WindoW visible
master.mainloop()
