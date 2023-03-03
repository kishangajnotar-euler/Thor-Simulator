import can 
import canID
from FreeRTOSinit import *
from structure import *

# CAN0 - Charger - vehicle 
# CAN1 - changer - inside 
class pycan:
    def __init__(self, name, btype, bitrate) -> None:
        self.bus = can.interface.Bus(name, bustype = btype, bitrate = bitrate)

#For linux 
CAN_1 = pycan(name='can0', btype='socketcan', bitrate=250000).bus
CAN_2 = pycan(name='can1', btype='socketcan', bitrate=250000).bus

# For windows 
# pycan(name='can0', bustype='socketcan', bitrate=250000) #use this 
# CAN_1 = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)  
# CAN_2 = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS2', bitrate=250000)  


#filers for can2
filters_can2 = [
             {"can_id": 0x72C, "can_mask": 0x72C << 5, "extended": False},
             {"can_id": 0x1AC, "can_mask": 0x1AC << 5, "extended": False},
             {"can_id": 0x18FF50E5, "can_mask": ((0x18FF50E5 & 0x18FF50E5) >> 13) << 16 | (((0x18FF50E5 & 0x00001FFF) << 3) | 0x04), "extended": True}]
CAN_2.set_filters(filters_can2)
filters_can1 = [
            {"can_id": 0x111, "can_mask": 0x111 << 5, "extended": False},
            {"can_id": 0x502, "can_mask": 0x502 << 5, "extended": False},
            {"can_id": 0x503, "can_mask": 0x503 << 5, "extended": False},
            {"can_id": 0x1806E5F4, "can_mask": ((0x1806E5F4 & 0x1806E5F4) >> 13) << 16 | (((0x1806E5F4 & 0x1806E5F4) << 3) | 0x04), "extended": True},
            #{"can_id": 0x56F4, "can_mask": ((0x1806E5F4 & 0x1806E5F4) >> 13) << 16 | (((0x1806E5F4 & 0x1806E5F4) << 3) | 0x04), "extended": True},
            {"can_id": 0x1CEC56F4, "can_mask": ((0x1CEC56F4 & 0x1CEC56F4) >> 13) << 16 | (((0x1CEC56F4 & 0x1CEC56F4) << 3) | 0x04), "extended": True},
            {"can_id": canID.GBT_BHM_CAN_ID, "can_mask": ((canID.GBT_BHM_CAN_ID & canID.GBT_BHM_CAN_ID) >> 13) << 16 | (((canID.GBT_BHM_CAN_ID & canID.GBT_BHM_CAN_ID) << 3) | 0x04), "extended": True},
            {"can_id": canID.GBT_BRM_CAN_ID, "can_mask": ((canID.GBT_BRM_CAN_ID & canID.GBT_BRM_CAN_ID) >> 13) << 16 | (((canID.GBT_BRM_CAN_ID & canID.GBT_BRM_CAN_ID) << 3) | 0x04), "extended": True},
            {"can_id": canID.GBT_BCP_CAN_ID, "can_mask": ((canID.GBT_BCP_CAN_ID & canID.GBT_BCP_CAN_ID) >> 13) << 16 | (((canID.GBT_BCP_CAN_ID & canID.GBT_BCP_CAN_ID) << 3) | 0x04), "extended": True},
            {"can_id": canID.GBT_BRO_CAN_ID, "can_mask": ((canID.GBT_BRO_CAN_ID & canID.GBT_BRO_CAN_ID) >> 13) << 16 | (((canID.GBT_BRO_CAN_ID & canID.GBT_BRO_CAN_ID) << 3) | 0x04), "extended": True},
            {"can_id": canID.GBT_BCL_CAN_ID, "can_mask": ((canID.GBT_BCL_CAN_ID & canID.GBT_BCL_CAN_ID) >> 13) << 16 | (((canID.GBT_BCL_CAN_ID & canID.GBT_BCL_CAN_ID) << 3) | 0x04), "extended": True},
            {"can_id": canID.GBT_BCS_CAN_ID, "can_mask": ((canID.GBT_BCS_CAN_ID & canID.GBT_BCS_CAN_ID) >> 13) << 16 | (((canID.GBT_BCS_CAN_ID & canID.GBT_BCS_CAN_ID) << 3) | 0x04), "extended": True},
            {"can_id": canID.GBT_BSM_CAN_ID, "can_mask": ((canID.GBT_BSM_CAN_ID & canID.GBT_BSM_CAN_ID) >> 13) << 16 | (((canID.GBT_BSM_CAN_ID & canID.GBT_BSM_CAN_ID) << 3) | 0x04), "extended": True},
            {"can_id": canID.GBT_BST_CAN_ID, "can_mask": ((canID.GBT_BST_CAN_ID & canID.GBT_BST_CAN_ID) >> 13) << 16 | (((canID.GBT_BST_CAN_ID & canID.GBT_BST_CAN_ID) << 3) | 0x04), "extended": True},
            {"can_id": canID.GBT_BSD_CAN_ID, "can_mask": ((canID.GBT_BSD_CAN_ID & canID.GBT_BSD_CAN_ID) >> 13) << 16 | (((canID.GBT_BSD_CAN_ID & canID.GBT_BSD_CAN_ID) << 3) | 0x04), "extended": True}
            ]
# CAN_1.set_filters(filters_can1)

#filters for can1

if __name__ == "__main__":
    createTasks()
    createEvent()
    stask()
    createTimers()
    