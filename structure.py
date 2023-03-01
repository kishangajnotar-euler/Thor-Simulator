from enum import Enum
import multiprocessing

numberofBMSTempSensors =  6
#this is for xeventgroup wait 
system_event_group = multiprocessing.Event()
system_event_group.set()
initial_sanity_check_bit = 0b0001
runtime_sanity_check_bit = 0b0010

#this is for state of chargerState
# class chargerState_t(Enum):
#     sanityState=0
#     idleState=1
#     userAuthState=2
#     waitingforvehiclestateDC=3
#     waitingforvehiclestateAC=4
#     chargingState=5
#     emergencyState=6
#     displayBillState=7
#     disconnectedstate=8
#     chargingcompletestate=9
#     errorcodestate=10
#     chargingcompletestateAC=11

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

class chargerState_t():
    state = 1
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
class GBT_STAGE(Enum):
    HANDSHAKE = 0
    CONFIG = 1
    CHARGING = 2
    END = 3
    ERRORS = 4

class charger_info_t:
    def __init__(self):
        # self.list = None
        # self.can_info = None
        self.state = None
        self.charger_request_state = None
        # self.handle_mutex = None
        # self.channel_info_config = None
        self.a_f_b_info = None
        self.channel_com_info = None
        self.channel_info = None
        # self.multi_packets_info = None
        self.settings = None
        # self.report_status_chain = None
        self.stamp = 0
        self.stamp_1 = 0
        self.stamp_2 = 0
        self.send_stamp = 0
        self.send_stamp_1 = 0
        self.start_send_cst_stamp = 0
        # self.charger_op_ctx = None
        # self.charger_op_ctx_gun_lock = None
        self.idle_op_state = None
        self.chm_op_state = None
        self.cro_op_state = None
        self.csd_cem_op_state = None
        self.bhm_received = 0
        self.brm_received = 0
        self.bcp_received = 0
        self.bro_received = 0
        self.bcl_received = 0
        self.bcs_received = 0
        self.bsm_received = 0
        self.bst_received = 0
        self.bsd_received = 0
        self.bem_received = 0
        self.precharge_voltage = 0
        self.precharge_action = 0
        self.auxiliary_power_state = 0
        self.gun_lock_state = 0
        self.power_output_state = 0
        self.gun_connect_state = 0
        self.gun_connect_state_debounce_count = 0
        self.gun_connect_state_update_stamp = 0
        self.door_state = 0
        self.error_stop_state = 0
        self.gb = 0
        self.test_mode = 0
        self.precharge_enable = 0
        self.fault = 0
        self.charger_power_on = 0
        self.manual = 0
        self.adhesion_test = 0
        self.double_gun_one_car = 0
        self.cp_ad = 0
        self.charger_output_voltage = 0
        self.charger_output_current = 0
        self.auxiliary_power_type = 0
        self.module_output_voltage = 0
        self.channel_max_output_power = 0
        self.module_output_current = 0
        self.bms_connect_retry = 0


class crm_data_t:
    def __init__(self):
        self.crm_result = 0
        self.charger_sn = 0




bmsdata = BMSDataParams()

#charger State 
chargerState = chargerState_t()
deviceParams=thorParams()
deviceParams.chargerType=1
deviceParams.chargingMode = 1
SanityCheckErr=SanityCheckErr_t()
#chargerState=chargerState_t.userAuthState