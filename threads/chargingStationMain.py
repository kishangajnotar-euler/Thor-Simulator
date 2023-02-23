from functions import *
from main import CAN_2
from main import initial_sanityevent, runtime_sanityevent, chargerState
import can 
import canID
import time

def idleTask():
    while True: 
        emergencyP = False
        if (emergencyP):
            buffer = [0] * 8
            message = can.Message(arbitration_id=canID.rx_6k6_charger, data=buffer, is_extended_id=True)
            CAN_2.send(message)
            setscreen()
        time.sleep(0.1)

def chargerLoop():
    initial_sanityevent.wait()
    runtime_sanityevent.wait()
    while (True):
        #IdleState
        if chargerState.state == 1:
            handleIdleState()
        #userAuthState
        elif chargerState.state == 2:
            handleAuthState_noRFID()
        #charging state
        elif chargerState.state == 3:
            handleChargingState()
        elif chargerState.state == 4: 
            handleEmergencyState()
        elif chargerState.state == 5:
            handleDisplayBill()
        else:
            #something went horrible wrong 
            pass

def telemetryParser():
    while(1):
        time.sleep(3)
        xServerString="1,2,3,4,5,6,7,8,9"
        if xServerString[2] ==  8:
            syncDateTime()

def type1Task():
    system_event_group.wait()
    bits_to_wait_for = initial_sanity_check_bit | runtime_sanity_check_bit
    while not (system_event_group.is_set() & bits_to_wait_for):
        system_event_group.wait()
    
    while(1):
        syncDateTime()

     



    

