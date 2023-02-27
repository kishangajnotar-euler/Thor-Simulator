from main import CAN_1
from main import CAN_2
import can
import canID
import time
from structure import*
rxBMSData = [0] * 8

def starkTXCallback():
    while(True):
        ack = [0x79]

        print("Transmit on can 1 stark tx")
        msg = can.Message(arbitration_id=canID.tx_stark, data=ack)
        CAN_1.send(msg)
        buffer = [0] * 8
        buffer[0] = canID.FC_ID
        print("Transmit on can 2 start tk")
        msg = can.Message(arbitration_id=canID.tx_Sync, data=buffer, is_extended_id=False)
        CAN_2.send(msg)
        time.sleep(0.5)

def chargerTXCallback():

    print("charger Tx call back")
    if chargerState.state==3:
        buffer=[0]*8
        msg = can.Message(arbitration_id=canID.tx_6k6_charger, data=buffer,is_extended_id=True)
        CAN_2.send(msg)
        time.sleep(0.5)
    if deviceParams.chargerType == 1 :
        global rxBMSData
        msg = can.Message(arbitration_id=canID.tx_6k6_charger, data=rxBMSData,is_extended_id=True)
        CAN_2.send(msg)
    elif deviceParams.chargerType == 2:
        buffer=[0]*8
        buffer[0] = 1
        buffer[1] = canID.FC_ID
        msg = can.Message(arbitration_id=canID.tx_NMT_Start, data=buffer,is_extended_id=False)
        CAN_2.send(msg)


        buffer[0] = canID.FC_ID
        buffer[1] = 0
        msg = can.Message(arbitration_id=canID.tx_Sync, data=buffer,is_extended_id=False)
        CAN_2.send(msg)


        for i in range(0,4):
            buffer[i]=buffer[i]+1
        for i in range(4,8):
            buffer[i]=buffer[i]+1
        time.sleep(0.02)
        msg = can.Message(arbitration_id=canID.tx_RPDO1, data=buffer,is_extended_id=False)
        CAN_2.send(msg)

        for i in range(4,8):
            buffer[i]=0

        time.sleep(0.02)
        msg = can.Message(arbitration_id=canID.tx_RPDO2, data=buffer,is_extended_id=False)
        CAN_2.send(msg)
 

