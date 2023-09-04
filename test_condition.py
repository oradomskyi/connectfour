from time import sleep
from threading import Thread, Lock
from random import randint

class A:
    def __init__(self):
        self.id = randint(0,100)

    def go(self):
        while True:
            delay = randint(1,100)/50
            #print(self.id, "sleeping", delay)
            sleep(delay)
            if lock.acquire() :
                print(self.id)#, "got lock")
                
                lock.release()
                #print(self.id, "releasea lock")

        

lock = Lock()
a = A()
b = A()
c = A()

t1 = Thread(target=a.go)
t2 = Thread(target=b.go)
t3 = Thread(target=c.go)

t1.start()
t2.start()
t3.start()
