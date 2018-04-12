#!/usr/bin/python
from Tkinter import *
import ScrolledText
import sys
import core

#Global variable section
SEPARATOR = '*'*75
typeList = [ "md5", "sha1", "sha256", "sha512"]
PASSWORD_FILE = "common-passwords.txt"

# GUI code section
class RedirectText(object):
    def __init__(self, widget):
        self.output = widget
        self.defstdout = sys.stdout

    def flush(self):
        self.defstdout.flush()

    def write(self, string):
        self.output.insert(END, string)

class MyApp(object):
    def __init__(self, parent):
        self.root = parent
        self.root.title("Crack4Beginner")
        self.var = IntVar()
        self.pwd_str = StringVar()
        self.InitGUI()

    def init_pwd_list(self):
        pwd_list = []
        # Load the password list
        with open(PASSWORD_FILE, 'rb') as file:
            pwd_list = [i.strip() for i in file]
        return pwd_list

    def run(self):
        index = int(self.var.get())
        string = str(self.pwd_str.get())
        lists = self.init_pwd_list()
        coreFunc = core.CoreFunc(string, typeList[index], lists)
        coreFunc.run()

    def InitGUI(self):

        # INPUT HEADER
        Label(self.root, text=SEPARATOR).pack(fill='x')
        Label(self.root, text="INPUT", font="Helvetica 12 bold").pack(fill='x')
        Label(self.root, text=SEPARATOR).pack(fill='x')

        # PassWord field
        Label(self.root, text="Password").pack(anchor=W)
        pwd_entry = Entry(self.root, textvariable=self.pwd_str)
        pwd_entry.pack(anchor=W)

        # Hash algorithm selection
        Label(self.root, text="Hash algorithm type").pack(anchor=W)
        radioList = []
        for i in range(len(typeList)):
            radioList.append(Radiobutton(self.root, text=typeList[i], variable=self.var, value=i))
            radioList[i].pack(anchor=W)
        self.var.set(0)

        # Panel contains 2 buttons for Run and Quit
        panel_bottom = PanedWindow(self.root, orient=HORIZONTAL)
        panel_bottom.pack(fill=BOTH, expand=1, side=BOTTOM)

        run_button = Button(self.root, text="Run", command=self.run)
        panel_bottom.add(run_button, stretch='always')

        quit_button = Button(self.root, text="Quit", command=self.root.quit)
        panel_bottom.add(quit_button, stretch='always')

        # Scrollbar for the list box
        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side=RIGHT, fill='y')

        # Redirect stdout
        panel = ScrolledText.ScrolledText(self.root, bg='grey', height='300')
        panel.pack(fill=BOTH)

        redir = RedirectText(panel)
        sys.stdout = redir


if __name__ == '__main__':
    root = Tk()
    root.geometry("400x600")
    app = MyApp(root)
    root.mainloop()
