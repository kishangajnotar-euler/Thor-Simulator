from tmp_declaration import *

def handleIdleState():
    while (1):
        chargerState = chargerState_t.userAuthState
        break
        if isEmergencyPressed():
            chargerState = chargerState_t.emergencyState
            break
        setScreen(chargerAvailable)
        if readElectronCardSerialID() == 0:
            chargerState        = userAuthState
            cardSerialNumber[8] = 0
            snprintf(deviceParams.uuid, 14, "%s", cardSerialNumber)
            break
        else :
            delay_milliSec(pdMS_TO_TICKS(RFIDRetryTime))

def handleAuthState_noRFID():
    while requestedChargeState() == TwoWaySwitchStates.DefaultPosition:
		#Display, Select correct charging mode
        #setScreen(selectChargingMode)
        print("screen set to selectChargingMode")
        #delay_milliSec(pdMS_TO_TICKS(100))
        if SanityCheckErr.errcount!=0:
            #setScreen(sanityError)
            print("screen set to sanityError")
            chargerState = chargerState_t.errorcodestate
            break
    if requestedChargeState()==TwoWaySwitchStates.DCCharge :
        chargerState = chargerState_t.waitingforvehiclestateDC

    elif requestedChargeState()==TwoWaySwitchStates.ACCharge:
        #turnOnACContactor()
        print("turn on an connector")
        chargerState = chargerState_t.waitingforvehiclestateAC

def handleWaitingforVehicleStateDC():
    while(1):
        #setScreen(waitingforVehicleDC)
        print("set screen to waitingforvehicalDC")
        #delay_milliSec(pdMS_TO_TICKS(1000))
        if SanityCheckErr.errcount!=0:
            #setScreen(sanityError)
            print("set screen to sanity error")
            chargerState = chargerState_t.errorcodestate; 
            break 
            
        if requestedChargeState() != deviceParams.chargingMode:
            # Send Type 4
            # sendStringType4()
            # turnOffACContactor()
            print("sendscreentype4 and  turnOFFac connector")
            chargerState = chargerState_t.userAuthState
            break
        if (xTaskGetTickCount() - lastBMSSync) < pdMS_TO_TICKS(BMSTimeout_ms) and lastBMSSync!=0 :
        
            chargerState = chargerState_t.chargingState
            break
        elif (xTaskGetTickCount() - lastBMSSync) > pdMS_TO_TICKS(BMSTimeout_ms):
                #Vehicle Disconnected
                sendStringType0(vehicleBMSDataTimeout)
                sendStringType4()
                #break
	


