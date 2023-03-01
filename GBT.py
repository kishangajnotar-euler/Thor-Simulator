from structure import GBT_STAGE, charger_info_t
import time
from gbt_structure import *
from main import CAN_1
import can
import canID
GBT_Stage = GBT_STAGE.HANDSHAKE
charger_info = charger_info_t()

def bms_data_settings_init():
    settings.dst=0xf4
    settings.src=0x56
    settings.chm_data.version_0 = 80
    settings.chm_data.version_1 = 25

    settings.crm_data.crm_result = 50.0
    settings.crm_data.charger_sn = 5

    settings.cts_data.S = 0xff
    settings.cts_data.M = 0xff
    settings.cts_data.H = 0xff
    settings.cts_data.d = 0xff
    settings.cts_data.m = 0xff
    settings.cts_data.Y = 0xffff

    settings.cml_data.max_output_voltage = 7500
    settings.cml_data.min_output_voltage = 2000
    settings.cml_data.max_output_current = 4000 - (100 * 10)
    settings.cml_data.min_output_current = 4000 - int(2.5 * 10)

    settings.ccs_data.output_voltage = 6640
    settings.ccs_data.output_current = 4000 - 192
    settings.ccs_data.total_charge_time = 13
    settings.ccs_data.u1.s.charge_enable = 0x01

def prepare_state_cts_cml():
    charger_info.bro_received=0
    bro_data.bro_reasult=0

def prepare_state_cro():
    cro_data.cro_reasult=0x00
    charger_info.bcl_received=0
    charger_info.bcs_received=0
    charger_info.cro_op_state=1

def send_cts():
    msg=charger_info.settings.cts_data
    message = can.Message(arbitration_id=canID.GBT_CTS_CAN_ID, data=msg, is_extended_id=True)
    CAN_1.send(message)

def send_cml():
    msg=cml_data
    message = can.Message(arbitration_id=canID.GBT_CML_CAN_ID, data=msg, is_extended_id=True)
    CAN_1.send(message)

def send_cro():
    msg=cro_data
    message = can.Message(arbitration_id=canID.GBT_CML_CAN_ID, data=msg, is_extended_id=True)
    CAN_1.send(message)

def handleHandshake():
    pass
def handleConfig():
    prepare_state_cts_cml()
    while(1):
        if charger_info.bcp_received==1:
            while(GBT_Stage==GBT_STAGE.CONFIG):
                send_cts()
                time.sleep(1)
                send_cml()
                time.sleep(1)
                if charger_info.bro_received==1 :
                    break
                #if error
            prepare_state_cro()
            while(GBT_Stage==GBT_STAGE.CONFIG):
                #if error
                send_cro()
                time.sleep(1)
                if bro_data.bro_reasult == 170 :
                    cro_data.cro_reasult=170
                    send_cro()
                    time.sleep(1)
                    break
            break
        # if error 
        else :
            send_crm()
            time.sleep(1)
    if GBT_Stage==GBT_STAGE.CONFIG:
        GBT_Stage=GBT_STAGE.CHARGING
                

def GBTask():
    can_data = [0] * 8
    bms_data_settings_init()
    while True: 
        if GBT_Stage == GBT_STAGE.HANDSHAKE: 
            handleHandshake()
            pass
        elif GBT_Stage == GBT_STAGE.CONFIG:
            handleConfig()
            pass
        elif GBT_Stage == GBT_STAGE.CHARGING:
            pass
        elif GBT_Stage == GBT_STAGE.END:
            pass
        elif GBT_Stage == GBT_STAGE.ERRORS:
            pass
        else:
            break
    pass