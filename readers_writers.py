from threading import Thread
from threading import Lock
from datetime import datetime
import time
import random
date_lock = Lock()
read_count_lock = Lock()
write_count_lock = Lock()
entry_lock = Lock()

# Operativsystem, labb 4 
# Nora Wennerström (nowe2200)
# 2023-12-18

# Källa för kodens struktur: Wikipedia, "Readers-writers problem." [Online]. Tillgänglig: https://en.wikipedia.org/wiki/Readers%E2%80%93writers_problem

# global datetime variable
shared_resource = ""
read_counter = 0
write_counter = 0

class WriteThread(Thread):
    def run(self):
        global shared_resource
        global write_counter

        for i in range(10):
            time.sleep(random.randint(0,3)/10)

            # entry section
            write_count_lock.acquire()
            write_counter += 1

            if(write_counter == 1):
                entry_lock.acquire()
                print("writethread locked the entry section")
            else:
                print("writethread bypassed the entry section lock")

            write_count_lock.release()

            date_lock.acquire()
            print("writethread entered the critical section")

            shared_resource = datetime.now() # critical section
            print("writethread exits the critical section")
            date_lock.release()

            # exit section
            write_count_lock.acquire()
            write_counter -= 1

            if(write_counter == 0):
                entry_lock.release()
                print("writethread unlocked the entry section")
            
            write_count_lock.release()




class ReverseWriteThread(Thread):
    def run(self):
        global shared_resource
        global write_counter

        for i in range(10):
            time.sleep(random.randint(0,3)/10)

            # entry section
            write_count_lock.acquire()
            write_counter += 1

            if(write_counter == 1):
                entry_lock.acquire()
                print("reversewritethread locked the entry section")
            else:
                print("reversewritethread bypassed the entry section lock")

            write_count_lock.release()

            date_lock.acquire()
            print("reversewritethread entered the critical section")

            shared_resource = datetime.now().strftime('%f.%S:%M:%H %d-%m-%Y') # critical section
            print("reversewritethread exits the critical section")
            date_lock.release()

            # exit section
            write_count_lock.acquire()
            write_counter -= 1

            if(write_counter == 0):
                entry_lock.release()
                print("reversewritethread unlocked the entry section")
            
            write_count_lock.release()

 


class ReadThread(Thread):
    def run(self):
        global shared_resource
        global read_counter
        global write_counter

        for i in range(10):
            time.sleep(random.randint(0,3)/10)

            # entry section
            entry_lock.acquire()
            print("readthread locked the entry section")
            
            read_count_lock.acquire()
            read_counter += 1

            if(read_counter == 1):
                date_lock.acquire()
                print("readthread locked the resource")
            else:
                print("readthread bypassed the resource lock")

            read_count_lock.release()
            entry_lock.release()
            print("readthread unlocked the entry section")

            print("global variable is ", shared_resource) # critical section

            # exit section
            read_count_lock.acquire()
            read_counter -= 1
            
            if(read_counter == 0):
                date_lock.release()
                print("readthread unlocked the resource")
            
            read_count_lock.release()
            



def main():
    threads = []
    
    wt = WriteThread()
    threads.append(wt)
    wt.start()

    rwt = ReverseWriteThread()
    threads.append(rwt)
    rwt.start()

    for i in range(5):
        t = ReadThread()
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    global shared_resource
    print("global variable is", shared_resource)

main()
