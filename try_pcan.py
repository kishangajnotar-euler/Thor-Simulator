import can

def message_handler(msg):
    print("hello")
    print(msg)

CAN_1 = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)  
msg = CAN_1.recv()
while(msg): 
    print("CAN 1", msg)
    msg = CAN_1.recv()
    if msg != None:
        pass
# filters_can1 = [
#              {"can_id": 0x111, "can_mask": 0x111 << 5, "extended": False},
#              {"can_id": 0x502, "can_mask": 0x502 << 5, "extended": False},
#              {"can_id": 0x503, "can_mask": 0x503 << 5, "extended": False},
#              {"can_id": 0x1806E5F4, "can_mask": ((0x1806E5F4 & 0x1806E5F4) >> 13) << 16 | (((0x1806E5F4 & 0x1806E5F4) << 3) | 0x04), "extended": True}]
# CAN_1.set_filters(filters_can1)
#notifier = can.Notifier(CAN_1, [message_handler])

# Keep the script running
while True:
    pass
