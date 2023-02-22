from main import CAN_2 as bus
from screen import setscreen
import can 
import canID
def idleTask():
    while True: 
        emergencyP = False
        if (emergencyP):
            buffer = [0] * 8
            message = can.Message(arbitration_id=canID.rx_6k6_charger, data=buffer, is_extended_id=True)
            bus.send(message)
            setscreen()

