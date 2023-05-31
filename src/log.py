import logging
import os
from datetime import datetime

def CreateLogger(filename):
    logger = logging.getLogger(filename)

    if len(logger.handlers) > 0:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    today = datetime.today().strftime("%Y%m%d%H")

    logdir = os.path.join(os.getcwd(), "log")
    todayfiledir = os.path.join(logdir, str(today))

    if not os.path.isdir(todayfiledir):
        os.mkdir(todayfiledir)

    fileHandler = logging.FileHandler( os.path.join(todayfiledir, str(filename)+".log"))
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    return logger

def infoLogging(filename, filemsg):
    logger = CreateLogger(filename)
    logger.info(filemsg)

