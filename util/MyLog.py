import logging
import getpass
import sys



class MyLog(object):

    def __init__(self):
        user = getpass.getuser()
        self.logger = logging.getLogger(user)
        self.logger.setLevel(logging.DEBUG)
        logFile = sys.argv[0][0:-3] + '.log'
        fromatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s')

        """
            输出日志到屏幕
        """
        logHand = logging.FileHandler(logFile)
        logHand.setFormatter(fromatter)
        logHand.setLevel(logging.ERROR)
        logHandst = logging.StreamHandler()
        logHandst.setFormatter(fromatter)
        self.logger.addHandler(logHand)
        self.logger.addHandler(logHandst)

    def debug(self, msg):
        self.logger.debug(msg)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warn(self, msg):
        self.logger.warn(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def critical(self, msg):
        self.logger.critical(msg)

if __name__ == "__main__":
    
    nylog = MyLog()
    nylog.debug("我叫胡建")
    nylog.error("出现错误")