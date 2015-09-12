import time
tells = []
class Tell:
    def __init__(self):
        #super(Tell, self).__init__(self)
        self.name = "tell"
        self.help = "leaves a message"
    def callback(self, user, args):
        try:
            TellMsg(user, args[1], time.time(), ' '.join(args[2:]))
            return "I will tell him the next time I see him"
        except:
            return "Something went wrong. Did you enter in the command correctly?"

class TellMsg:
    def __init__(self, sender, to, time, message):
        self.to = to
        self.sender = sender
        self.time = time
        self.message = message
        tells.append(self)