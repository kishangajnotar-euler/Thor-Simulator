from main import CAN_2 as bus
from main import bmsdata
from utils import read_float
import canID
def can2():
    msg = bus.recv()
    while(msg): 
        print("CAN 2 ", msg)
        msg = bus.recv()
        if msg != None:
            if msg.arbitration_id == canID.rx_TPDO1:
                bmsdata.ChargerVoltage = 