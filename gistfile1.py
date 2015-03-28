from __future__ import division, print_function
 
import sys, os, time, random, math, socket, string, pickle
import itertools
import json


players = []
ops = []
voices = []

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
        self.server = 'spoon.netsoc.tcd.ie'
        self.host = host
        self.port = port
 
        self.nickName = 'Scionbot'
        self.ident = 'gaygay2'
        self.realName = 'gaygay2'
 
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
        temp = self.socket.recv(1024)
        if len(temp) > 0: print("Temp: ", temp)
        self.receiveBuffer += temp
        temp = string.split(temp, "\n")
 
        for line in temp:
            try:
                line = string.rstrip(line)
                line = string.split(line)
 
                if(line[0] == "PING"):
                    self.socket.send("PONG %s\r\n" % line[1])
                elif line[1]=="MODE":
                    self.socket.send("JOIN #scion \r\n")
                    self.socket.send("JOIN #scion-ooc \r\n")
                    self.socket.send("PRIVMSG nickserv :identify Scionbot numberseverywhere\r\n")
                    if line[2]=="#scion" and line[3].count('+o') > 0:
                        if not (line[4] in ops):
                            ops.append(line[4])
                    elif line[2]=="#scion" and line[3].count('-o') > 0:
                        if line[4] in ops:
                            ops.remove(line[4])
                    elif line[2]=="#scion" and line[3].count('+v') > 0:
                        if not (line[4] in ops):
                            voices.append(line[4])
                    elif line[2]=="#scion" and line[3].count('-v') > 0:
                        if line[4] in ops:
                            voices.remove(line[4])
                if line[1] == "JOIN":
                    #code salvaging
                    userbits = string.split(line[0].lstrip(':'),'!')
                    user = userbits[0]
                    if user != self.nickName:
                        Player(user)
                elif line[1] == "353":
                    if line[4] == "#scion" and line[2] == self.nickName:
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
                            self.send("PRIVMSG #scion :deleted player with name " + user)
                elif line[1] == "NICK":
                    print ("asdasdasd")
                    userbits = string.split(line[0].lstrip(':'),'!')
                    user = userbits[0]
                    for player in players:
                        if player.name == user:
                            player.name = line[2]
                            self.send("PRIVMSG #scion :player " + user + " renamed to " + line[2].lstrip(':'))
                        # update ops list
                        [line[2].lstrip(':') if i == player.name else i for i in ops]
                        [line[2].lstrip(':') if i == player.name else i for i in voices]
            except:
                pass
        temp = ""

 
 
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

            userbits = prefix.split('!')
            user = userbits[0]
            affect = text[0]
            try:
                if user in ops:
                    stat = filter(lambda x: x.isalpha(), text[0])
                    x = int(affect[:-1 * len(stat)])
                    for player in players:
                        if text[1] == player.name:
                            player.stats[stat] += x
                            player.stats[stat] = max(player.stats[stat], 0)
                            self.sendMsg(channel, player.name + "'s " + stat + " stat has been changed to " + str(player.stats[stat]))
            except ValueError:
                pass

# gg2 strats pro af
class Player:
    def __init__(self, name):
        self.name = name
        self.stats = {
            "Hp":100,
            "Mag":100,
            "Str":100,
            "Def":100,
            "Res":100,
            "Spd":100,
            "Lck":100
        }
        players.append(self)
        print ("created player with name " + self.name)
        pyBot.send("PRIVMSG #scion :created player with name " + "self.name" + " and stats " + json.dumps(self.stats))
 
pyBot = Bot()
 
pyBot.connect()
pyBot.receive()
 
print("Connecting...")
 
while True:
    pyBot.receive()
    pyBot.handleInput()
    pyBot.receiveBuffer = ""
    pyBot.timer = time.time()