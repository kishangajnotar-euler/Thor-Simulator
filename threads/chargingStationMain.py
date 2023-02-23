import threading
from structure import *
from main import CAN_2 as bus
from main import initial_sanityevent, runtime_sanityevent, chargerState
from screen import setscreen
from main import deviceParams
import can 
import canID
import time

def syncDateTime():
    # sTime = RTC_TimeTypeDef()
    # DateToUpdate = RTC_TimeTypeDef()
    buffer = [0] * 8
    buffer[0] = 15
    buffer[1] = 7
    buffer[2] = 30
    buffer[5] = 22
    buffer[6] = 2
    buffer[7] = 2023
    #Transmit_on_CAN2(rx_calander_param, S, buffer, 8)
    message = can.Message(arbitration_id=canID.rx_calander_param, data=buffer, is_extended_id=False)
    bus.send(message)

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
    chargerState.state = 3

def setTTFC():
    ttfc=205
    mins=ttfc%60
    hours=ttfc/60
    buffer=[0]*8
    buffer[0] = hours
    buffer[1] = mins
    buffer[2] = hours
    buffer[3] = mins
    message = can.Message(arbitration_id=canID.rx_bill_param, data=buffer, is_extended_id=False)
    bus.send(message)

def setEnergyConsumed():
    energyConsumed_can=25.75
    buffer=[0]*8  
    buffer[0] = energyConsumed_can & 0xFF
    buffer[1] = (energyConsumed_can >> 8) & 0xFF
    message = can.Message(arbitration_id=canID.rx_energy_consumed, data=buffer, is_extended_id=False)
    bus.send(message)

def setBillAmount():
    billAmount=1234
    billAmount_int = int(billAmount * 100)
    buffer=[0]*8
    # Total Bill
    buffer[4] = billAmount_int & 0xFF
    buffer[5] = (billAmount_int >> 8) & 0xFF
    buffer[6] = (billAmount_int >> 16) & 0xFF
    buffer[7] = (billAmount_int >> 24) & 0xFF
    # Running
    buffer[0] = billAmount_int & 0xFF
    buffer[1] = (billAmount_int >> 8) & 0xFF
    buffer[2] = (billAmount_int >> 16) & 0xFF
    buffer[3] = (billAmount_int >> 24) & 0xFF
    message = can.Message(arbitration_id=canID.rx_bill_amount, data=buffer, is_extended_id=False)
    bus.send(message)

def handleEmergencyState():
    setscreen()
    time.sleep(1)
    setscreen()

def setUsername():
    username="kishan"
    userlen=len(username)
    username_can=username
    message = can.Message(arbitration_id=canID.rx_username_lower, data=username_can, is_extended_id=False)
    bus.send(message)
    if userlen > 8:
        message = can.Message(arbitration_id=canID.rx_username_upper, data=username_can, is_extended_id=False)
        bus.send(message)
    else :
        buffer = [0] * 8
        message = can.Message(arbitration_id=canID.rx_username_upper, data=buffer, is_extended_id=False)
        bus.send(message)

def setMarkType3Data():
    setUsername()
    time.sleep(1)
    setBillAmount()
    time.sleep(1)
    setTTFC()
    time.sleep(1)
    setEnergyConsumed()
    time.sleep(1)
    setscreen()

def setMarkType4Data():
    setUsername()
    time.sleep(1)
    setEnergyConsumed()
    time.sleep(1)
    setscreen()

def handleDisplayBill():
    count=0
    while(1):
        count=count+1
        if count==100:
            break
        setMarkType4Data()


def idleTask():
    while True: 
        emergencyP = False
        if (emergencyP):
            buffer = [0] * 8
            message = can.Message(arbitration_id=canID.rx_6k6_charger, data=buffer, is_extended_id=True)
            bus.send(message)
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

def type1Task():
    system_event_group.wait()
    bits_to_wait_for = initial_sanity_check_bit | runtime_sanity_check_bit
    while not (system_event_group.is_set() & bits_to_wait_for):
        system_event_group.wait()
    
    while(1):
        syncDateTime()

def chargerCanTask():
    while(1):
        if chargerState.state==3:
            buffer=[0]*8
            msg = can.Message(arbitration_id=canID.tx_6k6_charger, data=buffer,is_extended_id=True)
            CAN_2.send(msg)
            time.sleep(0.5)
        if deviceParams.chargerType == 1 :
            rxBMSData=[0]*8
            rxBMSData[2] = 3
            rxBMSData[3] = 2
            msg = can.Message(arbitration_id=canID.tx_6k6_charger, data=rxBMSData,is_extended_id=True)
            CAN_2.send(msg)
            time.sleep(1)
        elif deviceParams.chargerType == 2:
            buffer=[0]*8
            buffer[0] = 1
            buffer[1] = canID.FC_ID
            msg = can.Message(arbitration_id=canID.tx_NMT_Start, data=buffer,is_extended_id=False)
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
            buffer[7]=4
            msg = can.Message(arbitration_id=canID.tx_RPDO2, data=buffer,is_extended_id=False)
            CAN_2.send(msg)
            time.sleep(0.02)        


def handleChargingState():
    setscreen()
    while (1):
        time.sleep(5)
        setMarkType3Data()
        time.sleep(1)
        if deviceParams.chargingMode== 1:
            time.sleep(3)
            chargerCanTask=threading.Thread(target=chargerCanTask)
        time.sleep(0.1)
    

