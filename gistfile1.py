from __future__ import division, print_function

import sys, os, time, random, math, socket, string, pickle
import itertools

def parsemsg(s):
    # Stolen from Twisted. Parses a message to it's prefix, command and arguments.

    """Breaks a message from an IRC server into its prefix, command, and arguments.
    """
    prefix = ''
    trailing = []
    if s == "":
        return "", "", ""
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)
    return prefix, command, args

class Bot:

    def __init__(self, host='irc.esper.net', port=6667):
        self.server = 'spoon.netsoc.tcd.ie'
        self.host = host
        self.port = port

        self.nickName = 'Scionbot'
        self.ident = 'Scionbot'
        self.realName = 'Scionbot'

        self.receiveBuffer = ""

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.timer = 0

    def connect(self):
        self.socket=socket.socket( )
        self.socket.connect((self.host, self.port))
        self.socket.send("NICK %s\r\n" % self.nickName)
        self.socket.send("USER %s %s bla :%s\r\n" % (self.ident, self.host, self.realName))


    def send(self, msg):
#        print('sending:'+msg+"\r\n")
        self.socket.send('{0}\r\n'.format(msg).encode())


    def sendMsg(self, chan, msg):
        sendString = "PRIVMSG "+chan+" :"+msg
        self.send(sendString)


    def receive(self):
        temp = self.socket.recv(1024)
        self.receiveBuffer += temp
        temp = string.split(temp, "\n")

        for line in temp:
            try:
                line = string.rstrip(line)
                line = string.split(line)

                if(line[0] == "PING"):
                    self.socket.send("PONG %s\r\n" % line[1])
                    print("PONG %s\r\n" % line[1])
            except:
                pass


    def handleInput(self):
        prefix, command, args = parsemsg(self.receiveBuffer)

        if command == "PRIVMSG":

            channel = args[0]

            inputString = args[1]
            inputString = inputString[:-2]
            text = inputString.split(" ")

            roll = text[0]
            try:
                n_dice = min(int(roll[:-1]), 25)
                if roll[-1] == "d":
                    output = []
                    for i in range(n_dice):
                        output.append(random.randint(1, 10))
                    output.sort()
                    output = ", ".join([str(len(list(group)))+"("+str(name)+")" for name, group in itertools.groupby(output)])
                    self.sendMsg(channel, output)
            except ValueError:
                pass


pyBot = Bot()

pyBot.connect()
pyBot.receive()

print("Connecting...")

pyBot.timer = time.time()

while True:
    pyBot.receive()
    pyBot.socket.send("JOIN #scion \r\n")
    pyBot.socket.send("JOIN #scion-ooc \r\n")
    pyBot.handleInput()
    pyBot.receiveBuffer = ""