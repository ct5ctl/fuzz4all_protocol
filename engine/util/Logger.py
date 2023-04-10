import os


class Logger:
    # TODO: support logging levels
    def __init__(self, basedir, validation=False):
        if validation:
            self.logfile = os.path.join(basedir, "log_validation.txt")
        else:
            self.logfile = os.path.join(basedir, "log.txt")

    def log(self, msg, out=False):
        with open(self.logfile, "a+") as logfile:
            logfile.write(msg)
            logfile.write("\n")
        if out:
            print(msg)

    def logo(self, msg):
        self.log(str(msg), True)