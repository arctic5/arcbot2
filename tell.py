import time
tells = []
class Tell:
    def __init__(self):
        self.name = "tell"
        self.help = "leaves a message"
    def callback(self, user, args):
        TellMsg(user, args[1], time.time(), ' '.join(args[2:]))
        return True

class TellMsg:
    def __init__(self, sender, to, time, message):
        self.to = to
        self.sender = sender
        self.time = time
        self.message = message
        tells.append(self)
#        pyBot.sendMsg(pyBot.chan, "message left for " + to)