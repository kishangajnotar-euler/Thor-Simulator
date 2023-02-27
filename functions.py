import time
import threading
from structure import *
from main import CAN_2 as bus
import can
import canID
from structure import chargerState
import pandas as pd
energytaski = 0
chargerFlag = False


chargerCantask = None
def setscreen():
    buffer=[0]*8
    buffer[0]  = 2
    buffer[1]  = 0
    message = can.Message(arbitration_id=canID.rx_Screen_id, data=buffer, is_extended_id=False)
    bus.send(message)
    print("Updating screen")

def syncDateTime():
    # sTime = RTC_TimeTypeDef()
    # DateToUpdate = RTC_TimeTypeDef()
    buffer = [0] * 8
    buffer[0] = 15
    buffer[1] = 7
    buffer[2] = 30
    buffer[5] = 22
    buffer[6] = 2
    buffer[7] = 20
    #Transmit_on_CAN2(rx_calander_param, S, buffer, 8)
    message = can.Message(arbitration_id=canID.rx_calander_param, data=buffer, is_extended_id=False)
    bus.send(message)

def setTTFC():
    ttfc=205
    mins=int(ttfc%60)
    hours=int(ttfc/60)
    buffer=[0]*8
    buffer[0] = hours
    buffer[1] = mins
    buffer[2] = hours
    buffer[3] = mins
    message = can.Message(arbitration_id=canID.rx_bill_param, data=buffer, is_extended_id=False)
    bus.send(message)

def setEnergyConsumed():
    df = pd.read_csv('energyMeter.csv')

    if energytaski > len(energytaski):
        energyConsumed_can=int(df.iloc[-1]['value']*100)
        chargerFlag = True
    else:
        energyConsumed_can=int(df.iloc[energytaski]['value']*100)
        energytaski = energytaski + 1

    buffer=[0]*8  
    buffer[0] = (energyConsumed_can & 0xFF)
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

def setUsername():
    username="hey"
    userlen=len(username)
    username_can=list(username)
    buffer = [0] * 8
    message = can.Message(arbitration_id=canID.rx_username_lower, data=buffer, is_extended_id=False)
    bus.send(message)
    if userlen > 8:
        message = can.Message(arbitration_id=canID.rx_username_upper, data=username_can, is_extended_id=False)
        bus.send(message)
    else :
        
        message = can.Message(arbitration_id=canID.rx_username_upper, data=buffer, is_extended_id=False)
        bus.send(message)
    print("-------------- USER NAME SENT -------------------")

def setMarkType3Data():
    print("setMarkType3Data")
    setUsername()
    time.sleep(0.1)
    setBillAmount()
    time.sleep(0.1)
    setTTFC()
    time.sleep(0.1)
    setEnergyConsumed()
    time.sleep(0.1)
    setscreen()

def setMarkType4Data():
    print("setMarkType4Data")
    setUsername()
    time.sleep(0.1)
    setEnergyConsumed()
    time.sleep(1)
    setscreen()

def handleDisplayBill():
    count=0
    while(1):
        print("Inside Handle diplay billl -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ")
        count=count+1
        if count > 10:
            chargerState.state = 1
            break
        setMarkType4Data()

def handleEmergencyState():
    setscreen()
    time.sleep(0.1)
    setscreen()

def handleIdleState():
    chargerState.state = 2

def handleAuthState_noRFID():
    counter = 0
    counterL = 100
    while True: 
        setscreen()
        time.sleep(0.1)
        counter = counter + 1
        if counter >= counterL:
            break 
    chargerState.state = 3

def handleChargingState():
    global chargerCantask
    setscreen()
    count = 0
    countL = 5
    while (1):
        print("Handle charging state")
        time.sleep(1)
        setMarkType3Data()
        time.sleep(1)
        print(f"-------------------------------------------------------------------------------------------- ")
        if deviceParams.chargingMode == 1 and chargerCantask == None:
            print(" -------------------------------- TASK created -----------------------------------")
            time.sleep(3)
            chargerCantask=threading.Thread(target=chargerCanTask)
            chargerCantask.start()
        time.sleep(0.1)
        if chargerFlag:
            print("changing state from charging to idle ========================================")
            chargerState.state = 5
            chargerCantask.join()
            break






def chargerCanTask():
    while(1):
        print("chargerCanTask")
        if chargerState.state!=3:
            buffer=[0]*8
            msg = can.Message(arbitration_id=canID.tx_6k6_charger, data=buffer,is_extended_id=True)
            bus.send(msg)
            break
        if deviceParams.chargerType == 1 :
            global rxBMSData
            msg = can.Message(arbitration_id=canID.tx_6k6_charger, data=rxBMSData,is_extended_id=True)
            bus.send(msg)
            time.sleep(1)
        elif deviceParams.chargerType == 2:
            buffer=[0]*8
            buffer[0] = 1
            buffer[1] = canID.FC_ID
            msg = can.Message(arbitration_id=canID.tx_NMT_Start, data=buffer,is_extended_id=False)
            bus.send(msg)

            for i in range(0,4):
                buffer[i]=buffer[i]+1
            for i in range(4,8):
                buffer[i]=buffer[i]+1
            time.sleep(0.02)
            msg = can.Message(arbitration_id=canID.tx_RPDO1, data=buffer,is_extended_id=False)
            bus.send(msg)

            for i in range(4,8):
                buffer[i]=0
            buffer[7]=4
            msg = can.Message(arbitration_id=canID.tx_RPDO2, data=buffer,is_extended_id=False)
            bus.send(msg)
            time.sleep(0.02)
     