import time as T
from constants import *

def tickValue(x):
    return round( (x*1000)/TICK_RATE )

def currTicks():
    return tickValue(time())

def timeFromTick(x):
    return x*TICK_RATE

def time():
    return T.time()