import multiprocessing as mp

import numpy as np
import random
from time import sleep

class ProcessObject:

    # function that initialize the ProcessObject
    def __init__(self, ID, N,  db):
        self._ID = ID # Process ID
        self._N = N # number of processes
        self._db = db # database objest
        self._logClock = random.randint(0, self._N*3) # local logic clock
        self._counter = 0 # number of database entries
        self._readPipes = [] # list of reading pipes
        self._writePipes = [] # list of writing pipes
        self._recvMessageList = [] # list od received messages
        self._helpList = [] # help list od received messages
        self._messageHistory = [] # list  of all send and received messages
        self._isOver = False # is this process been 5 times in the database

        self.initPipeList() # initialization od Pipe lists

    # function that initialize the Pipe lists
    def initPipeList(self):
        for i in range(self._N):
            self._readPipes.append(0)
            self._writePipes.append(0)

    # function that starts the Process
    def startProcess(self):

        #self._logClock = 4 # help initalization

        print("ID: {} started, initial logClock : {}".format(self._ID, self._logClock)) # printing the initial message

        self._messageHistory.append("{} started, initial logClock : {}\n".format(self._ID, self._logClock)) # adding the message

        # operative loop
        for i in range(5):

            request = self.createMessage("request") # creating request message

            self.sendMessageToAll(request) # sending the messages to all other processes

            sleep(1)

            responseCounter = 0 # response counter

            # loop where to receive the messages
            while True:
                self.recvMessageFromAll() # putting all the received messages in the list

                # loop for decoding and answering the reveived messages
                for m in range(len(self._recvMessageList)):
                    message = self._recvMessageList.pop(0) # get the first message in the list
                    #print("ID: {} = {}".format(self._ID, message)) # print the message

                    otherID = int(self.getMessageElement(message, 0)) # get the ID of the process how send the message
                    otherClock = int(self.getMessageElement(message, 1)) # get the clock of the process how send the message
                    theMessage = self.getMessageElement(message, 2) # get the message


                    if theMessage == "request":

                        if self._logClock > otherClock or self._logClock == otherClock and self._ID > otherID:
                            response = self.createMessage("response") # creating response
                            self.sendMessageTo(otherID, response) # sending to the process how sent the message
                            self._logClock = max(self._logClock, otherClock) + 1  # update clock

                        else:
                            self._helpList.append(message) # putting the message in list for later
                            #print("ID: {} = helplist {}".format(self._ID, self._helpList))

                    if theMessage == "response":
                        responseCounter += 1
                        self._logClock = max(self._logClock, otherClock) + 1  # update clock



                if responseCounter == self._N - 1:

                    #print("ID {} , log clock: {}".format(self._ID, self._logClock)) # help print

                    # wait if the database is not free
                    while True:
                        if self._db.isFree():
                            break

                    self.enterDataBase() # entering the database

                    # loop for decoding and answering the other messages
                    for m in range(len(self._helpList)):
                        message = self._helpList.pop(0) # get the first message in the list
                        #print("ID: {} = {}".format(self._ID, message))

                        otherID = int(self.getMessageElement(message, 0)) # get the ID of the process how send the message
                        otherClock = int(self.getMessageElement(message, 1)) # get the clock of the process how send the message
                        theMessage = self.getMessageElement(message, 2) # get the message

                        if theMessage == "request":
                            response = self.createMessage("response") # creating response
                            self.sendMessageTo(otherID, response) # sending to the process how sent the message

                        sleep(1)
                    break

            sleep(self._N - 2)



        textfile = open("zad{}.txt".format(self._ID), "w") # opening the text file

        # print all the messages in the text file
        for m in self._messageHistory:
            textfile.write(str(m))
        textfile.write("ID: {} is over".format(self._ID))

        textfile.close() # closing the text file

    # function that sends a message to another process
    def sendMessageTo(self, ID, message):
        self._messageHistory.append("sending to {} {}\n".format(ID, message))
        self._writePipes[ID].send(message) # sending the message in the pipe

    # function that receives a message from another process
    def recvMessageFrom(self, ID):
        if(self._readPipes[ID].poll()):
            return self._readPipes[ID].recv() # receiving the message in the pipe

    # function that sends a message to all tbe otheres process
    def sendMessageToAll(self, message):
        for i in range(self._N):
            if i != self._ID:
                self.sendMessageTo(i, message)

    # function that receives a message from all the otheres process
    def recvMessageFromAll(self):
        for i in range(self._N):
            if i != self._ID:
                message = self.recvMessageFrom(i)
                if message is not None:
                    self._messageHistory.append("receiving: {}\n".format(message))
                    self._recvMessageList.append(message)

    # function that increases the counter
    def increaseCounter(self):
        self._counter += 1

    # function where the process enters the database
    def enterDataBase(self):
        self.increaseCounter()
        self._Free = False # clossing the database
        self._db.getCounters()[self._ID] = self._counter # updating the counter
        self._db.getLogClocks()[self._ID] = self._logClock # udpdating the logic clock
        self._db.printdb() # printing the database
        sleep(np.random.uniform(0.1, 2)) # sleeping
        self._Free = True # opening the database

    # function that create the message
    def createMessage(self, message):
        return "{}|{}|{}".format(self._ID, self._logClock, message)

    # function that get the needed message element
    def getMessageElement(self, message, element):
        s = str(message)
        return s.split("|")[element]



class DataBase:

    # function that initialize the DataBase
    def __init__(self, N):
        self._N = N # number of processes
        self._counters = mp.Array('i', [0]*N) # array of counters
        self._logClocks = mp.Array('i', [0]*N) # array of log clocks
        self._Free = True # is the database open or close

    # function that returns the counters
    def getCounters(self):
        return self._counters

    # function that returns the logic clocks
    def getLogClocks(self):
        return self._logClocks

    # function that returns database status
    def isFree(self):
        return self._Free

    # function that prints the database
    def printdb(self):
        print("DataBase")
        for i in range(self._N):
            print("ID {}: counter = {}, log clock = {}".format(i, self._counters[i], self._logClocks[i]))

# main function
if __name__ == '__main__':
    print("Main")

    N = 5 # number of processes

    db = DataBase(N) # initializing the database

    db.printdb() # printing the database

    Processes = [] # list of processes

    # initializing the processes
    for i in range(N):
        p = ProcessObject(i, N, db)
        Processes.append(p)

    # help print
    #for i in range(N):
        #print("{}: ID:{}".format(i, Processes[i]._ID))

    #print(len(Processes)) # help print

    # creating the pipes for all the processes
    for p1 in Processes:
        for p2 in Processes:
            if p1 == p2:
                continue

            readPipe, writePipe = mp.Pipe(duplex = False)

            p1._readPipes[p2._ID] = readPipe
            p2._writePipes[p1._ID] = writePipe

    # staring the processes
    for p in Processes:
        pro = mp.Process(target=p.startProcess).start()



