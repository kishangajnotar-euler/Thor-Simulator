from main import CAN_1 as bus
from main import bmsdata
def can1():
    msg = bus.recv()
    while(msg): 
        print("CAN 1", msg)
        msg = bus.recv()
        if msg != None:
            #set event bit
            pass