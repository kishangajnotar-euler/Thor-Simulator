from main import CAN_2 as bus
from structure import bmsdata
from utils import read_float
import canID
from data_log import write_in_log
def can2():
    msg = bus.recv()
    while(msg): 
        # print("CAN 2 ", msg)
        msg = bus.recv()
        # print("can 2", msg)
        if msg != None:
            write_in_log(msg)
            if msg.arbitration_id == canID.rx_TPDO1:
                bmsdata.ChargerVoltage = read_float(msg, 0)
                bmsdata.ChargerCurrent = read_float(msg, 4)
            elif msg.arbitration_id == canID.rx_FC_status:
                pass

