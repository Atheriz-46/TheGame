import time as T
from constants import *

def tickValue(x):
    return round( (x*1000)/TICK_RATE )

def currTicks():
    return tickValue(time())

def timeFromTick(x):
    return round(x*TICK_RATE/1000,5)

def time():
    return round(T.time(),5)