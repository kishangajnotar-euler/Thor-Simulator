from main import CAN_1
from main import CAN_2
import can
import canID
import time
def starkTXCallback():
    while(True):
        ack = [0x79]
        msg = can.Message(arbitration_id=canID.tx_stark, data=ack)
        CAN_1.send(msg)
        buffer = [0] * 8
        buffer[0] = canID.FC_ID
        msg = can.Message(arbitration_id=canID.tx_Sync, data=buffer)
        time.sleep(0.5)