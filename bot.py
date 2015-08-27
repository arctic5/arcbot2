from __future__ import division, print_function
 
import sys, os, time, random, math, socket, string, pickle
import itertools
import json

#plugins
import tell


players = []
ops = []
voices = []
commands = []
helps = []
commandCallbacks = []
ignore = ['dzjin']

#todo: json based base stat loading maybe?

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
        self.host = host
        self.port = port
 
        self.nickName = 'Scionbot'
        self.ident = 'gaygay2'
        self.realName = 'gaygay2'
        self.chan =  "#gg2test"
 
        self.receiveBuffer = ""
 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
        self.timer = 0
 
    def connect(self):
        self.socket=socket.socket( )
        self.socket.connect((self.host, self.port))
        self.socket.send("NICK %s\r\n" % self.nickName)
        self.socket.send("USER %s %s bla :%s\r\n" % (self.ident, self.host, self.realName))
 
 
    def send(self, msg):
        self.socket.send('{0}\r\n'.format(msg).encode())
 
 
    def sendMsg(self, chan, msg):
        sendString = "PRIVMSG "+chan+" :"+msg
        self.send(sendString)
 
 
    def receive(self):
        self.temp = self.socket.recv(1024)
        # if len(self.temp) > 0: print("Temp: ", self.temp)
        self.receiveBuffer += self.temp
        self.temp = string.split(self.temp, "\n")
 
        for line in self.temp:
            try:
                line = string.rstrip(line)
                line = string.split(line)
 
                if(line[0] == "PING"):
                    self.socket.send("PONG %s\r\n" % line[1])
                elif line[1]=="MODE":
                    self.socket.send("JOIN %s \r\n" % self.chan)
                    if line[2]== self.chan and line[3].count('+o') > 0:
                        if not (line[4] in ops):
                            ops.append(line[4])
                    elif line[2]== self.chan and line[3].count('-o') > 0:
                        if line[4] in ops:
                            ops.remove(line[4])
                    elif line[2]== self.chan and line[3].count('+v') > 0:
                        if not (line[4] in ops):
                            voices.append(line[4])
                    elif line[2]== self.chan and line[3].count('-v') > 0:
                        if line[4] in ops:
                            voices.remove(line[4])
                if line[1] == "JOIN":
                    #code salvaging
                    userbits = string.split(line[0].lstrip(':'),'!')
                    user = userbits[0]
                    if user != self.nickName:
                        Player(user)
                elif line[1] == "353":
                    if line[4] ==  self.chan and line[2] == self.nickName:
                        for i in line[5:]:
                            i = i.lstrip(':')
                            if i[0]=='@':
                                ops.append(i.lstrip('@'))
                            if i[0]=='+':
                                voices.append(i.lstrip('+'))
                            if i != self.nickName:
                                i = i.lstrip('@')
                                i = i.lstrip('+')
                                Player(i)
                elif line[1] == "PART":
                    print ("asdasdasd")
                    userbits = string.split(line[0].lstrip(':'),'!')
                    user = userbits[0]
                    for player in players:
                        if player.name == user:
                            players.remove(player)
                            self.send("PRIVMSG %s :deleted player with name " + user % self.chan)
                elif line[1] == "NICK":
                    print ("asdasdasd")
                    userbits = string.split(line[0].lstrip(':'),'!')
                    user = userbits[0]
                    for player in players:
                        if player.name == user:
                            player.name = line[2]
                            #self.send("PRIVMSG %s :player " + user + " renamed to " + line[2].lstrip(':') % self.chan)
                        # update ops list
                        [line[2].lstrip(':') if i == player.name else i for i in ops]
                        [line[2].lstrip(':') if i == player.name else i for i in voices]
            except:
                pass
    def addCommand(self, command):
        # takes a class that looks like this
        # command: "name"
        # help: "documentation"
        # callback: 
        self.command = command()
        commands.append(self.command.name)
        helps.append(self.command.help)
        commandCallbacks.append(self.command.callback)
 
 
    def handleInput(self):
        self.prefix, self.command, self.args = parsemsg(self.receiveBuffer)
        if self.command == "PRIVMSG":
            self.channel = self.args[0]
            self.userbits = self.prefix.split('!')
            self.user = self.userbits[0]
            self.hostmask = self.userbits[1]
            self.inputString = self.args[1]
            self.inputString = self.inputString[:-2]
            self.text = self.inputString.split(" ")
            self.msgstring = ' '.join(self.text)
 
            # make messages pretty
            print ('<' + self.user + '> ' + str(self.text[0]))
            if self.user not in ignore:
                if self.msgstring[0] == '!':
                    _cmd = self.text[0][1:]
                    cmd = _cmd.lower()
                    # help command
                    if cmd in commands:
                        i = commands.index(cmd)
                        commandCallbacks[i](self.user, self.text)
                    elif cmd == "help":
                        self.sendMsg(self.chan, str(commands))
                    else:
                        self.sendMsg(self.chan, "No such command")
            # hard code for right now but modularize it later
        if self.command == "PRIVMSG" or self.command == "JOIN":
            for i in tell.tells:
                if (i.to == self.user):
                    self.sendMsg(self.chan, str(i.to) + ", message from <" + str(i.sender) + "> " + str(i.message))
                    print(str(i.to) + ", message from <" + str(i.sender) + "> " + str(i.message))
                    tell.tells.pop(tell.tells.index(i))
                continue

        if self.command != 'PRIVMSG':
            print(self.temp[0])
        
        self.temp = ""

# gg2 strats pro af
class Player:
    def __init__(self, name):
        self.name = name
        players.append(self)
        print ("created player with name " + self.name)
        #pyBot.send("PRIVMSG %s :created player with name " + self.name + " and stats " + json.dumps(self.stats) % self.chan)
 
if __name__ == "__main__":
    pyBot = Bot()
    
    pyBot.connect()
    pyBot.receive()
    
    #load plugins
    pyBot.addCommand(tell.Tell)

    print("Connecting...")
     
    while True:
        pyBot.receive()
        pyBot.handleInput()
        pyBot.receiveBuffer = ""
        pyBot.timer = time.time()
