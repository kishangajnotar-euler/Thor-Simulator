from main import CAN_2 as bus
from main import initial_sanityevent, runtime_sanityevent, chargerState
from screen import setscreen
import can 
import canID
import time
def handleIdleState():
    chargerState.state = 2

def handleAuthState_noRFID():
    counter = 0
    counterL = 1e3
    while True: 
        setscreen()
        time.sleep(0.1)
        counter = counter + 1
        if counter >= counterL:
            break 
        

def handleEmergencyState():
    pass

def handleDisplayBill():
    pass

def idleTask():
    while True: 
        emergencyP = False
        if (emergencyP):
            buffer = [0] * 8
            message = can.Message(arbitration_id=canID.rx_6k6_charger, data=buffer, is_extended_id=True)
            bus.send(message)
            setscreen()

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



    

