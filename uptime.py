import time
import datetime
starttime = round(time.time())

class Uptime:
    def __init__(self):
        self.name = "uptime"
        self.help = "displays uptime"
    def callback(self, asdf, asdfg):
        return str(datetime.timedelta(seconds= round(time.time()) - starttime))
