import time as T
from .constants import *


def tickValue(x):
    """
    Used to get the number of ticks from time in seconds

    Args:
                    x (float) : Time in seconds
    """
    return round((x * 1000) / TICK_RATE)


def currTicks():
    """
    Used to get the number of ticks from current system time

    """
    return tickValue(time())


def timeFromTick(x):
    """
    Used to get the time in seconds from number of ticks

    Args:
                    x (int) : Number of ticks
    """
    return round(x * TICK_RATE / 1000, 5)


def time():
    """
    Used to get machine time

    """
    return round(T.time(), 5)
