from main import CAN_1 as bus
from structure import bmsdata
from utils import read_float
import BMSdata 
import canID
from data_log import write_in_log
from gbt_structure import brm_data, bcl_data, charger_info,mp_msg,bro_data,bcs_data,bsm_data

def parse_data(canmsg):
    print(canmsg)
    data = str(canmsg)[-41:-18].split(" ")
    data = [int(v,16) for v in data if v != '']
    print("--",data,"--")
    return data


def parse_can_brm(canmsg):
    data = canmsg
    # data = str(canmsg)[-41:-18].split(" ")
    # data = [int(v,16) for v in data]
    brm_data.version_1                   = ((float)(data[2] << 16) + (data[1] << 8) + data[0]) / 10.0
    brm_data.version_0                   = ((float)(data[2])) / 10.0
    brm_data.battery_type                = ((float)(data[3])) / 10.0
    # brm_data.total_battery_rate_capicity = ((float)((data[5] << 8) + data[4])) / 10.0
    # brm_data.total_battery_rate_voltage  = ((float)((data[7] << 8) + data[6])) / 10.0
    if charger_info.brm_received == 0: 
        charger_info.settings.crm_data.crm_result = 0xaa
        charger_info.brm_received = 1

def parse_can_bhm():
    charger_info.bhm_received = 1

def parse_can_bcl(canmsg):
    # data = str(canmsg)[-41:-18].split(" ")
    # data = [int(v,16) for v in data]
    data = canmsg
    charger_info.bcl_received = 1
    test = ((float)(data[3] << 8) + data[2])
    bcl_data.require_voltage= ((float)(data[1] << 8) + data[0]) / 10.0
    bcl_data.require_current= ((float)(data[3] << 8) + data[2]) / 10.0 - 40
    bcl_data.charge_mode=(data[4])

def parse_can_bst(canmsg):
    charger_info.bsd_received = 1

def parse_can_bcp():
    if charger_info.bcp_received==0:
        charger_info.bcp_received=1

def parse_can_bro(canmsg):
    bro_data.bro_reasult=canmsg[0]
    charger_info.bro_received=1

def parse_can_bcs(canmsg):
    charger_info.bcs_received=1
    bcs_data.charge_voltage=((float)(canmsg[1] << 8) + canmsg[0]) / 10.0
    bcs_data.charge_current= ((float)(canmsg[3] << 8) + canmsg[2]) / 10.0 - 40
    #bcs_data.u1.v   	   = ((float)(canmsg[5] << 8) + canmsg[4]) / 10.0
    bcs_data.soc		   = (float)(canmsg[6]) 
    bcs_data.remain_min    =((float)(canmsg[8] << 8) + canmsg[7])

def parse_can_bsm(can_data):
    charger_info.bsm_received=1
    bsm_data.single_max_voltage_group  = (float)(can_data[0])
    bsm_data.battery_max_temperature  = (float)(can_data[1])
    bsm_data.battery_max_temperature_sn  = (float)(can_data[2])
    bsm_data.battery_min_temperature  = (float)(can_data[3])
    bsm_data.battery_min_temperature_sn  = (float)(can_data[4])
    # bsm_data.u1.v  = (float)(can_data[5])
    # bsm_data.u2.v  = (float)(can_data[6])

def parse_can_bsd(canmsg):
    charger_info.bsd_received=1

def handle_j1939_mp_msg(canmsg):
    mp_total_size = (canmsg[1] << 8) + canmsg[2]
    mp_msg.size=canmsg[3]
    mp_msg.pgn=(canmsg[5] << 16) + (canmsg[6] << 8) + canmsg[7]
    mp_curr_size=0
    if mp_msg.pgn == 0x000200:
        parse_can_brm(mp_msg.data)
    if mp_msg.pgn == 0x000600:
        parse_can_bcp()
    if mp_msg.pgn == 0x001100:
        parse_can_bcs(mp_msg.data)

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
            if msg.arbitration_id == 0x1CEC56F4:
                # print(" ========================================================= ")
                # print ( "EXTENDED IDS ---------------------- ")
                # print(msg)

                # print("+++++++++++++++++++++++++++++++++++++++++++++++++")
                handle_j1939_mp_msg(parse_data(msg))
            if msg.arbitration_id == canID.GBT_BHM_CAN_ID:
                parse_can_bhm()
            if msg.arbitration_id == canID.GBT_BRM_CAN_ID:
                parse_can_brm(parse_data(msg))
            if msg.arbitration_id == canID.GBT_BCP_CAN_ID:
                parse_can_bcp()
            if msg.arbitration_id == canID.GBT_BRO_CAN_ID:
                parse_can_bro(parse_data(msg))
            if msg.arbitration_id == canID.GBT_BCL_CAN_ID:
                parse_can_bcl(parse_data(msg))
            if msg.arbitration_id == canID.GBT_BCS_CAN_ID:
                parse_can_bcs(parse_data(msg))
            if msg.arbitration_id == canID.GBT_BSM_CAN_ID:
                parse_can_bsm(parse_data(msg))
            if msg.arbitration_id == canID.GBT_BST_CAN_ID:
                parse_can_bst(msg.data)
            if msg.arbitration_id == canID.GBT_BSD_CAN_ID:
                parse_can_bsd(msg)
            
            
            
