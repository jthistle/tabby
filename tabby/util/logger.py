import logging

def get_logger():
    logger = logging.getLogger("debug")
    hdlr = logging.FileHandler("debug.log")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

    return logger

logger = get_logger()
