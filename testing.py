#!/usr/bin/python

import multiprocessing
import sys
import time
import getpass
from passlib.hash import md5_crypt as pwd_context

PASSWORD_FILE = "common-passwords.txt"

class Worker(multiprocessing.Process):
    def __init__(self, id, queue, pwd_hash, pwd_list):
        multiprocessing.Process.__init__(self)
        self.id = id
        self.queue = queue
        self.pwd_hash = pwd_hash
        self.pwd_list = pwd_list

    def run(self):
        proc_id = self.id
        print("Creating process %d" % self.id)
        try:
            num_procs = multiprocessing.cpu_count() * 2
            for i in self.pwd_list:
                if (not self.queue.empty()):
                    check = self.queue.get()
                    if (check is None):
                        print("[Process %d: Exiting...]\n" % proc_id)
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
        print("Time executed: {:.2f} minutes".format(end/60))
    else:
        print("Time executed: {} seconds".format(end))

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
    for p in processes:
        p.start()
    
    printTime(start_time)
    
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Shutdown")
        sys.exit()