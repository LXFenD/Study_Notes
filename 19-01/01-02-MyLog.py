import logging


class Testlogger:
    
    def __init__(self):
        logFormat = '%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s'
        logFileName = './testLog.txt'
        logging.basicConfig(level= logging.INFO, format=logFormat, filename= logFileName, filemode='w')
        logging.debug('debug mssage')
        logging.info('info mssage')
        logging.warning('warning mssage')
        logging.error('error mssage')
        logging.critical('critical mssage')

if __name__ == "__main__":
    tl = Testlogger()


