from main import CAN_1
import can
import canID
from main import GBT_Stage, charger_info
from structure import GBT_STAGE, crm_data_t
import time
from datetime import datetime, timedelta

crm_data = crm_data_t()

def send_crm(can_data: list) -> None:
    can_data[0] = crm_data.crm_result & 0xFF
    can_data[1] = crm_data.charger_sn & 0xFF
    can_data[2] = 0x00 & 0xFF
    can_data[3] = 0x00 & 0xFF
    can_data[4] = 0x00 & 0xFF
    can_data[5] = 0x68 & 0xFF
    can_data[6] = 0x69 & 0xFF
    can_data[7] = 0x76 & 0xFF
    can.Message(arbitration_id=canID.GBT_CRM_CAN_ID, data=can_data, is_extended_id=True)


def prepare_state_crm():
    global crm_data
    charger_info.brm_received = 0
    charger_info.bcp_received = 0
    crm_data.charger_sn = 6

def bms_data_settings_init():
    # charger_info.bhm_received = 1
    pass

def parse_state_chm():
    charger_info.bhm_received = 0.0
    charger_info.bst_received = 0.0 
    # chm_data.version

def send_chm(can_data: list):
    can_data[0] = 1
    can_data[1] = 1
    can_data[2] = 128
    mssg = can.Message(arbitration_id=canID.GBT_CHM_CAN_ID, data=can_data, is_extended_id=True)
    CAN_1.send(mssg)


def handleHandshake(can_data):
    global crm_data
    parse_state_chm()
    while (GBT_Stage == GBT_STAGE.HANDSHAKE):
        send_chm(can_data)
        time.sleep(0.25)
        if charger_info.bhm_received == 1:
            break
    prepare_state_crm()
    time.delay(0.5)
    xstart = datetime.now()
    while(GBT_Stage == GBT_STAGE.HANDSHAKE):
        if charger_info.brm_received == 1:
            crm_data.crm_result = 170
            send_crm(can_data)
            time.delay(1)
            break
        send_crm(can_data)
        time.delay(0.25)
        if (datetime.now() - xstart) > timedelta(seconds=1000*100):
            GBT_Stage = GBT_STAGE.ERRORS
            break
    if GBT_Stage == GBT_STAGE.HANDSHAKE:
        GBT_Stage = GBT_STAGE.CONFIG

def GBTask():
    bms_data_settings_init()
    can_data = [0] * 8
    while True: 
        if GBT_Stage == GBT_STAGE.HANDSHAKE: 
            handleHandshake(can_data)
            pass
        elif GBT_Stage == GBT_STAGE.CONFIG:
            pass
        elif GBT_Stage == GBT_STAGE.CHARGING:
            pass
        elif GBT_Stage == GBT_STAGE.END:
            pass
        elif GBT_Stage == GBT_STAGE.ERRORS:
            pass
        else:
            pass
    pass