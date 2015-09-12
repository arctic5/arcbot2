import random

class Roll:
    def __init__(self):
        #super(Tell, self).__init__(self)
        self.name = "roll"
        self.help = "displays random number from 1 - 100 or given number"
    def callback(self, user, args):
        try:
            if (len(args) == 1):
                args.append(100)
                print str(random.randint(1, args[1]))
            return user + " rolls " + str(random.randint(1, int(args[1]))) + " point(s)"
        except:
            return "Something went wrong. Did you enter in the command correctly?"