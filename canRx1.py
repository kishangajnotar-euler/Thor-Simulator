from main import CAN_1 as bus
from structure import bmsdata
from utils import read_float
import BMSdata 
import canID
def can1():
    msg = bus.recv()
    while(msg): 
        # global rxBMSData
        # print("CAN 1", msg)
        msg = bus.recv()
        # print(msg)
        if msg != None:
            if msg.arbitration_id == canID.rx_BMS_CHRGR:
                if (msg.data[4] == 0 and msg.data[5] == 0 and msg.data[6] == 0 and msg.data[7] == 0):
                    print("Updating BMS parameters ")
                    BMSdata.rxBMSData = str(msg)[-41:-18].split(" ")
                    BMSdata.rxBMSData = [int(v,16) for v in BMSdata.rxBMSData]
                    print(BMSdata.rxBMSData)
                    # print("BMS DATA ----------------------------------")
                    # print(rxBMSData)