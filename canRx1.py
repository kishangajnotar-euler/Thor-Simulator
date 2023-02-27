from main import CAN_1 as bus
from structure import bmsdata
from utils import read_float
from flashCharger import rxBMSData
import canID
def can1():
    msg = bus.recv()
    while(msg): 
        # print("CAN 1", msg)
        msg = bus.recv()
        if msg != None:
            if msg.arbitration_id == canID.rx_BMS_CHRGR:
                if (msg.data[4] == 0 and msg.data[5] == 0 and msg.data[6] == 0 and msg.data[7] == 0):
                    print("Updating BMS parameters ")
                    rxBMSData = msg.data