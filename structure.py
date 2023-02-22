from enum import Enum
numberofBMSTempSensors =  6


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

