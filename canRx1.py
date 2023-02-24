from main import CAN_1 as bus
from structure import bmsdata
from utils import read_float
def can1():
    msg = bus.recv()
    while(msg): 
        # print("CAN 1", msg)
        msg = bus.recv()
        if msg != None:
            pass