import time
import datetime
starttime = round(time.time())

class Uptime:
    def __init__(self):
        self.name = "uptime"
        self.help = "displays uptime"
    #todo: fix this
    def callback(self, user, args):
        return str(datetime.timedelta(seconds= round(time.time()) - starttime))
