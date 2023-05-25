import os


class Logger:
    # TODO: support logging levels
    def __init__(self, basedir, validation=False, verbose=True):
        if validation:
            self.logfile = os.path.join(basedir, "log_validation.txt")
        else:
            self.logfile = os.path.join(basedir, "log.txt")
        self.verbose = verbose

    def log(self, msg, out=False):
        try:
            with open(self.logfile, "a+") as logfile:
                logfile.write(msg)
                logfile.write("\n")
            if out and self.verbose:
                print(msg)
        except:
            pass

    def logo(self, msg):
        self.log(str(msg), True)
