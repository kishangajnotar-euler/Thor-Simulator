import multiprocessing
from tmp_declaration import *
from chargingStates import *



def chargingStationSanityTask():
    print("chargingStationSanityTask task created")

    #this is for xeventgroup wait
    system_event_group.wait()
    bits_to_wait_for = initial_sanity_check_bit | runtime_sanity_check_bit
    while not (system_event_group.is_set() & bits_to_wait_for):
        system_event_group.wait()
    # Bits are set, continue execution
    print("Bits are set, continuing execution.")

    #this is for state of chargerState
    while(1):
        if chargerState==chargerState_t.idleState:
            handleIdleState()
            break
        elif chargerState==chargerState_t.userAuthState:
            handleAuthState_noRFID()
            break
        elif chargerState==chargerState_t.waitingforvehiclestateDC:
            handleWaitingforVehicleStateDC()
            break
        elif chargerState==chargerState_t.waitingforvehiclestateAC:
            handleWaitingforVehicleStateAC()
            break
        elif chargerState==chargerState_t.chargingState:
            handleChargingState()
            break
        elif chargerState==chargerState_t.emergencyState:
            handleEmergencyState()
            break
        elif chargerState==chargerState_t.displayBillState:
            handleDisplayBill()
            break
        elif chargerState==chargerState_t.disconnectedstate:
            handleDisplayDisconnected()
            break
        elif chargerState==chargerState_t.chargingcompletestate:
            handleDisplayChargingComplete()
            break
        elif chargerState==chargerState_t.chargingcompletestateAC:
            handleDisplayChargingCompleteAC()
        else :
            break 
    
    #vTaskDelete(NULL)
