import can 
from FreeRTOSinit import *

# CAN0 - Charger - vehicle 
# CAN1 - changer - inside 
class pycan:
    def __init__(self, name, btype, bitrate) -> None:
        self.bus = can.interface.Bus(name, bustype = btype, bitrate = bitrate)

#For linux 
CAN_1 = pycan(name='can0', btype='socketcan', bitrate=250000).bus
CAN_2 = pycan(name='can1', btype='socketcan', bitrate=250000).bus
#filers for can2
filters = [
             {"can_id": 0x72C, "can_mask": 0x72C << 5, "extended": False},
             {"can_id": 0x1AC, "can_mask": 0x1AC << 5, "extended": False},

             {"can_id": 0x18FF50E5, "can_mask": ((0x18FF50E5 & 0x18FF50E5) >> 13) << 16 | (((0x18FF50E5 & 0x00001FFF) << 3) | 0x04), "extended": True}]
#filters for can1

CAN_2.set_filters(filters)

# For windows 
# pycan(name='can0', bustype='socketcan', bitrate=250000) use this 
# CAN_1 = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)  
# CAN_2 = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)  

if __name__ == "__main__":
    createEventGroups()
    createTasks()
    createTimers()
    vTaskStartScheduler()
    stask()