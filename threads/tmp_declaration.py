import threading
from enum import Enum

#this is for xeventgroup wait 
# system_event_group = multiprocessing.Event()
# system_event_group.set()
# initial_sanity_check_bit = 0b0001
# runtime_sanity_check_bit = 0b0010

#this is for state of chargerState
class chargerState_t(Enum):
    sanityState=0
    idleState=1
    userAuthState=2
    waitingforvehiclestateDC=3
    waitingforvehiclestateAC=4
    chargingState=5
    emergencyState=6
    displayBillState=7
    disconnectedstate=8
    chargingcompletestate=9
    errorcodestate=10
    chargingcompletestateAC=11

chargerState=chargerState_t.userAuthState

#all 9 functions for charging state whicg in chargingstationTest

#for handleIdleState
def isEmergencyPressed():
    return 0 #else return 0 // depend on user input

#for handleAuthState_noRFID
class TwoWaySwitchStates(Enum):
    DefaultPosition = 0  #NONE
    DCCharge        = 1  #DC Charging
    ACCharge        = 2  #AC Charging
    ErrorPosition   = 3  #Error
def requestedChargeState():
    return TwoWaySwitchStates.DefaultPosition
    #else return ACCharge // depends upon user input
class SanityCheckErr_t():
    errcount     =0
    errEM        =0
    errHUMIDITY  =0
    errTemp      =0
    errCharger   =0
    reserved     =0
SanityCheckErr=SanityCheckErr_t()

#for





