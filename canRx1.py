from main import CAN_1 as bus
from structure import bmsdata
from utils import read_float
import BMSdata 
import canID
from data_log import write_in_log
from main import charger_info
from structure import brm_data, bcl_data
def parse_can_brm(canmsg):
    data = str(canmsg)[-41:-18].split(" ")
    data = [int(v,16) for v in data]
    brm_data.version_1                   = ((float)(data[2] << 16) + (data[1] << 8) + data[0]) / 10.0
    brm_data.version_0                   = ((float)(data[2])) / 10.0
    brm_data.battery_type                = ((float)(data[3])) / 10.0
    brm_data.total_battery_rate_capicity = ((float)((data[5] << 8) + data[4])) / 10.0
    brm_data.total_battery_rate_voltage  = ((float)((data[7] << 8) + data[6])) / 10.0
    if charger_info.brm_received == 0: 
        charger_info.settings.crm_data.crm_result = 0xaa
        charger_info.brm_received = 1

def parse_can_bhm(canmsg):
    charger_info.bhm_received = 1

def parse_can_bcl(canmsg):
    data = str(canmsg)[-41:-18].split(" ")
    data = [int(v,16) for v in data]
    charger_info.bcl_received = 1
    test = ((float)(data[3] << 8) + data[2])
    bcl_data.require_voltage= ((float)(data[1] << 8) + data[0]) / 10.0
    bcl_data.require_current= ((float)(data[3] << 8) + data[2]) / 10.0
    bcl_data.charge_mode=(data[4])

def parse_can_bst(canmsg):
    charger_info.bsd_received = 1


def can1():
    msg = bus.recv()
    while(msg): 
        # global rxBMSData
        # print("CAN 1", msg)
        msg = bus.recv()
        # print(msg)
        if msg != None:
            write_in_log(msg)
            if msg.arbitration_id == canID.rx_BMS_CHRGR:
                if (msg.data[4] == 0 and msg.data[5] == 0 and msg.data[6] == 0 and msg.data[7] == 0):
                    print("Updating BMS parameters ")
                    BMSdata.rxBMSData = str(msg)[-41:-18].split(" ")
                    BMSdata.rxBMSData = [int(v,16) for v in BMSdata.rxBMSData]
                    print(BMSdata.rxBMSData)
                    # print("BMS DATA ----------------------------------")
                    # print(rxBMSData)
            if msg.arbitration_id == canID.GBT_BHM_CAN_ID:
                parse_can_bhm(msg)
            if msg.arbitration_id == canID.GBT_BRM_CAN_ID:
                parse_can_brm(msg)
            if msg.arbitration_id == canID.GBT_BCL_CAN_ID:
                parse_can_bcl(msg)
            if msg.arbitration_id == canID.GBT_BST_CAN_ID:
                parse_can_bst(msg)
