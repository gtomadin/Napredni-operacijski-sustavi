import multiprocessing as mp

import numpy as np
import random
from time import sleep

class Car:
    # function that initialize the Car class
    def __init__(self, ID, direction, carQueue):
        #print("init Car")
        self._ID = ID
        self._direction = direction
        self._carQueue = carQueue

    # function that starts the Car
    def startCar(self):
        rand = np.random.uniform(0.1, 2)
        sleep(rand) # sleep for sleep for a while
        s = "{}|{}|Waiting to pass the bridge".format(self._ID, self._direction) # create message
        print(s) # print message
        self._carQueue.put(s) # send message

        # waiting for the permission to pass the bridge
        while True:
            sleep(1)
            if self.messageFound("Passing the bridge"):
                break

        # passing the bridge
        while True:
            sleep(1)
            if self.messageFound("Bridge passed"):
                break

    # function that search for the message
    def messageFound(self, string):

        if not self._carQueue.empty():
            m = self._carQueue.get() # get the message

            # take all the elements of the message
            id = getmessElement(m, 0)
            dir = getmessElement(m, 1)
            text = getmessElement(m, 2)

            # if the message is relevant print it, if not send it back
            if self._direction == int(dir) and text == string:
                print("ID: {} direction: {} {}".format(id, dir, text))
                return True
            else:
                self._carQueue.put(m)



class Semaphore:
    # function that initialize the Semaphore class
    def __init__(self, N):
        print("init Semaphore")
        self._N = N # number of cars
        self._queue = mp.Queue() # help queue
        self._queuedir0 = mp.Queue() # queue for the 0 direction
        self._queuedir1 = mp.Queue() # queue for the 1 direction
        self._direction = random.randint(0,1) # random initial direction
        self._Cars = [] # list of cars

    # function that starts the Semaphore
    def startSemaphore(self):

        # create N cars with random directions
        for i in range(self._N):
            rand = random.randint(0, 1)
            car = Car(i, rand, mp.Queue())
            self._Cars.append(car)

        # starting all the Cars
        for i in range(self._N):
            p = mp.Process(target=self._Cars[i].startCar).start()

        # print initial direction
        print("initial direction: {}".format(self._direction))

        t = 0 # variable to facilitate reading

        while True:
            print("t = {}".format(t))
            self.getMessages() # read the messages

            # if there are not enough car wait
            if self._queuedir0.qsize() < 3 and self._queuedir1.qsize() < 3:
                rand = np.random.uniform(0.5, 1)
                sleep(rand)
                self.getMessages()

            # help print
            #print("dir0: {} dir1: {}".format(self._queuedir0.qsize(), self._queuedir1.qsize()))
            #print("dir {}".format(self._direction))

            # change the direction if there are less then 3 cars on this side and 3 or more cars on the other one
            if self._direction == 0 and self._queuedir0.qsize() < 3 and self._queuedir1.qsize() >= 3:
                self.changeDirection()

            # change the direction if there are less then 3 cars on this side and 3 or more cars on the other one
            if self._direction == 1 and self._queuedir1.qsize() < 3 and self._queuedir0.qsize() >= 3:
                self.changeDirection()

            # if there are no cars read the messages agian
            if self._queuedir0.qsize() == 0 and self._queuedir1.qsize() == 0:
                t = t + 1
                if t == 20:
                    break
                continue



            self.makePass() # make the cars pass
            self.changeDirection() # change direction
            if t == 20:
                break
            sleep(1)
            t = t+1


    # function that collect the messages
    def getMessages(self):

        # get all the messages and put them in the help queue
        for car in self._Cars:
            if not car._carQueue.empty():

                m = car._carQueue.get()
                #print("mess : {}".format(m))
                text = getmessElement(m, 2)
                if text == "Waiting to pass the bridge":
                    self._queue.put(m)
                else:
                    car._carQueue.put(m)

        #print("q size: {}".format(self._queue.qsize()))

        # put the messages in the right direction queue
        while True:
            if not self._queue.empty():

                message = self._queue.get()
                dir = str(getmessElement(message, 1))

                if dir == "0":
                    self._queuedir0.put(message)
                if dir == "1":
                    self._queuedir1.put(message)

            else:
                break

    # function that changes the direction
    def changeDirection(self):
        if self._direction == 0:
            self._direction = 1
        else:
            self._direction = 0

    # function that make the car pass
    def makePass(self):

        messages = [] # help list
        m = None # help variable

        # make three cars pass
        for i in range(3):
            if self._direction == 0 and not self._queuedir0.empty():
                m = self._queuedir0.get()
                #print("0 {}".format(m))
            elif self._direction == 1 and not self._queuedir1.empty():
                m = self._queuedir1.get()
                #print("1 {}".format(m))
            if(m != None):
                messages.append(m) # save messages for later
                id = getmessElement(m, 0)
                dir = getmessElement(m, 1)
                s = "{}|{}|Passing the bridge".format(id, dir) # create message
                self._Cars[int(id)]._carQueue.put(s) # send message
                m = None


        rand  = np.random.uniform(2, 3)
        sleep(rand) # sleep for a whale


        for mess in messages:
            id = getmessElement(mess, 0)
            dir = getmessElement(mess, 1)
            s = "{}|{}|Bridge passed".format(id, dir)# create message
            self._Cars[int(id)]._carQueue.put(s) # send messges

        sleep(2) # sleep for a whale



# function that get the needed message element
def getmessElement( message, elem):
    s = str(message)
    return s.split("|")[elem]

# main function
if __name__ == '__main__':
    print("Main")

    N = 20 # number of cars

    semaphore = Semaphore(N) # create the semaphore
    semaphore.startSemaphore()# start the semaphore

    #p = mp.Process(target=semaphore.startSemaphore).start()




