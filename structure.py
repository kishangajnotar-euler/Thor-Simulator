from enum import Enum
import multiprocessing

numberofBMSTempSensors =  6
#this is for xeventgroup wait 
system_event_group = multiprocessing.Event()
system_event_group.set()
initial_sanity_check_bit = 0b0001
runtime_sanity_check_bit = 0b0010

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

class chargerType_t(Enum):
    noCharger = 0
    slowCharger = 1
    fastCharger = 2


class BMSDataParams:
    def __init__(self):
        self.Cell_V_Min_Val = 0.0
        self.Cell_V_Max_Val = 0.0
        self.Pack_I_Master = 0.0
        self.Pack_Q_SOC_Trimmed = 0.0
        self.SOH = 0.0
        self.Pack_V_Sum_of_Cells = 0.0
        self.FullyChargeFlag = 0
        self.BMSStatus = 0
        self.BatteryCapacity = 0.0
        self.ChargerVoltage = 0.0
        self.ChargerCurrent = 0.0
        self.ChargerStatus = 0
        self.ChargerDetection = 0
        self.requestCurrent = 0.0
        self.requestedVoltage = 0.0
        self.Aux_T = [0.0] * numberofBMSTempSensors

class thorParams:
    def __init__(self):
        self.hwVersion = ""
        self.swVersion = ""
        self.hwIdentifier = ""
        self.chargingMode = 0
        self.emCount = 0
        self.emResponseLimit = 0
        self.chargerType = None
        self.uuid = ""
        self.lastPong = 0
        self.chargerType : chargerType_t

class chargerState_t(Enum):
    state = 0
    mapping = {0: "sanityState", 1:"idleState", 2:"userAuthState", 3:"chargingState", 4:"emergencyState", 5:"displayBillState"}
# class RTC_TimeTypeDef:
#     def __init__(self):
#         self.Hours = hours
#         self.Minutes = minutes
#         self.Seconds = seconds
#         self.TimeFormat = time_format
#         self.SubSeconds = subseconds
#         self.SecondFraction = second_fraction
#         self.DayLightSaving = daylight_saving
#         self.StoreOperation = store_operation

#bmsdata struct
bmsdata = BMSDataParams()

#charger State 
chargerState = chargerState_t(0)
deviceParams=thorParams()
deviceParams.chargerType=1
SanityCheckErr=SanityCheckErr_t()
#chargerState=chargerState_t.userAuthState