
import logging
import sys, traceback
import time
import functools


def create_error_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("*** arcpy_Error_Logger ***")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler(r"./error_logger.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)

    return logger

def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("*** arcpy_EVENT_Logger ***")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler(r"./logger.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger

def event_logger(log):

    '''
        A decorator that wraps the passed in function and logs
    arcpy events

    @param logger: The logging object
    '''

    def decorator(func):

        def wrapper(*args, **kwargs):
            msgs = "\n***********{}*****************\n".format(func.__name__)
            log.info(msgs)
            return func(*args, **kwargs)
        return wrapper

    return decorator


def arcpy_exception(log):

    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param log: The logging object
    """
    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # Get the traceback object
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                # Concatenate information together concerning the error into a message string
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                # Print Python error messages for use in Python / Python window
                log.exception(pymsg)

        return wrapper
    return decorator


def time_it():

    def decorator(func):

        def wrapper_timer(*args, **kwargs):
                starttime = time.perf_counter()
                value = func(*args, **kwargs)
                endtime = time.perf_counter()
                hours, rem = divmod(endtime - starttime, 3600)
                minutes, seconds = divmod(rem, 60)
                print("\t\t\tit took: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

                return value
        return wrapper_timer
    return decorator


