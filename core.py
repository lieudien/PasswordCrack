# Main function code section
from multiprocessing import *
import sys
import os
import time
import getpass
from cStringIO import StringIO
from passlib.hash import md5_crypt
from passlib.hash import bcrypt
from passlib.hash import sha256_crypt
from passlib.hash import sha512_crypt


class Worker(Process):
    def __init__(self, id, type, info_queue, print_queue, pwd_hash, pwd_list):
        Process.__init__(self)
        self.id = id
        self.info_queue = info_queue
        self.print_queue = print_queue
        self.type = type
        self.pwd_hash = pwd_hash
        self.pwd_list = pwd_list

    def printFunc(self, message):
        self.print_queue.put(message)

    def compareHash(self, string):
        if (self.type == "md5"):
            return md5_crypt.verify(string, self.pwd_hash)
        elif (self.type == "bcrypt"):
            return bcrypt.verify(string, self.pwd_hash)
        elif (self.type == "sha256"):
            return sha256_crypt.verify(string, self.pwd_hash)
        elif (self.type == "sha512"):
            return sha512_crypt.verify(string, self.pwd_hash)

    def run(self):
        proc_id = self.id
        self.printFunc("Creating process %d" % self.id)
        try:
            num_procs = cpu_count() * 2
            for i in self.pwd_list:
                if (not self.info_queue.empty()):
                    check = self.info_queue.get()
                    if (check is None):
                        self.printFunc("[Process %d: Exiting...]" % proc_id)
                        return

                if (self.compareHash(i)):
                    self.printFunc("[Process %d: Found: %s]" % (proc_id, i))
                    [self.info_queue.put(None) for j in range(num_procs - 1)]
                    return
        except KeyboardInterrupt:
            self.printFunc ("[Process %d : Shutdown by KeyboardInterrupt.]" % self.id)
            pass

class CoreFunc(object):

    def __init__(self, pwd_str, hash_type , pwd_list):
        self.pwd_str = pwd_str
        self.hash_type = hash_type
        self.pwd_list = pwd_list

    def encrypt(self, password, type):
        pwd_hash = ""
        if (type == "md5"):
            pwd_hash = md5_crypt.hash(password.strip())
        elif (type == "bcrypt"):
            pwd_hash = bcrypt.hash(password.strip())
        elif (type == "sha256"):
            pwd_hash = sha256_crypt.hash(password.strip())
        elif (type == "sha512"):
            pwd_hash = sha512_crypt.hash(password.strip())
        print("Type: {}. Your hash: {}".format(type, pwd_hash))
        return pwd_hash

    def printTime(self, start_time):
        end = time.time() - start_time
        if (end > 60):
            print("Time executed: {:.2f} minutes".format(end/60))
        else:
            print("Time executed: {} seconds".format(end))

    def run(self):
        processes = []
        # Establish communication queue
        info_queue = Queue()
        print_queue = Queue()
        print("-------------------------------------------------------")
        print("You type: {}...".format(self.pwd_str))
        pwd_hash = self.encrypt(self.pwd_str, self.hash_type)

        # Start worker processes
        num_procs = cpu_count() * 2

        size = len(self.pwd_list) / num_procs
        size = int(round(size, -1))
        for i in range(num_procs):
            lists = self.pwd_list[i*size: (i+1)*size]
            processes.append(Worker(i, self.hash_type, info_queue, print_queue, pwd_hash, lists))
            print("[Process %d has %d words]" % (i, len(lists)))

        start_time = time.time()
        [p.start() for p in processes]

        for w in processes:
            w.join()
        while (not print_queue.empty()):
            print (print_queue.get())
            sys.stdout.flush()

        self.printTime(start_time)
