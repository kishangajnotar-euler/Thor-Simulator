from main import GBT_Stage, charger_info
from structure import GBT_STAGE, crm_data_t
import time
from datetime import datetime, timedelta

crm_data = crm_data_t()

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
    #settings.ccs_data.u1.s.charge_enable = 0x01

def prepare_state_csd_cem():
    charger_info.bem_received=0
    charger_info.csd_cem_op_state=0

def prepare_state_cts_cml():
    charger_info.bro_received=0
    bro_data.bro_reasult=0

def prepare_state_cro():
    cro_data.cro_reasult=0x00
    charger_info.bcl_received=0
    charger_info.bcs_received=0
    charger_info.cro_op_state=1

def send_csd():
    msg=charger_info.settings.csd_data
    message = can.Message(arbitration_id=canID.GBT_CSD_CAN_ID, data=msg, is_extended_id=True)
    CAN_1.send(message)

def send_cst():
    msg=charger_info.settings.cst_data
    message = can.Message(arbitration_id=canID.GBT_CST_CAN_ID, data=msg, is_extended_id=True)
    CAN_1.send(message)

def send_cem():
    msg=cem_data
    message = can.Message(arbitration_id=canID.GBT_CEM_CAN_ID, data=msg, is_extended_id=True)
    CAN_1.send(message)
    
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
    message = can.Message(arbitration_id=canID.GBT_CRO_CAN_ID, data=msg, is_extended_id=True)
    CAN_1.send(message)


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

def parse_state_chm():
    charger_info.bhm_received = 0.0
    charger_info.bst_received = 0.0 
    chm_data.version_0=1
    chm_data.version_1=128
    charger_info.chm_op_state=0

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
    time.sleep(0.5)
    xstart = datetime.now()
    while(GBT_Stage == GBT_STAGE.HANDSHAKE):
        if charger_info.brm_received == 1:
            crm_data.crm_result = 170
            send_crm(can_data)
            time.sleep(1)
            break
        send_crm(can_data)
        time.sleep(0.25)
        if (datetime.now() - xstart) > timedelta(seconds=1000*100):
            GBT_Stage = GBT_STAGE.ERRORS
            break
    if GBT_Stage == GBT_STAGE.HANDSHAKE:
        GBT_Stage = GBT_STAGE.CONFIG

def handleConfig():
    xstart = datetime.now()
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
                if (datetime.now() - xstart) > timedelta(seconds=1000*100):
                    GBT_Stage = GBT_STAGE.ERRORS
                    break
            prepare_state_cro()
            while(GBT_Stage==GBT_STAGE.CONFIG):
                if (datetime.now() - xstart) > timedelta(seconds=1000*100):
                    GBT_Stage = GBT_STAGE.ERRORS
                    break
                send_cro()
                time.sleep(1)
                if bro_data.bro_reasult == 170 :
                    cro_data.cro_reasult=170
                    send_cro()
                    time.sleep(1)
                    break
            break
        elif (datetime.now() - xstart) > timedelta(seconds=1000*100):
            GBT_Stage = GBT_STAGE.ERRORS
            break
        else :
            send_crm()
            time.sleep(1)
    if GBT_Stage==GBT_STAGE.CONFIG:
        GBT_Stage=GBT_STAGE.CHARGING

def handleEnd():
    xstart = datetime.now()
    while(GBT_Stage==GBT_STAGE.END):
        prepare_state_csd_cem()
        if charger_info.bsd_received==1 :
            send_csd()
            time.sleep(1)
        elif (datetime.now() - xstart) > timedelta(seconds=1000*100):
            #cem_data.u4.s.bsd_timeout = 1;
            GBT_Stage = GBT_STAGE.ERRORS
            break
        else :
            send_cst()
            time.sleep(1)

def handleError():
    send_cem()
    time.sleep(1)

def GBTask():
    bms_data_settings_init()
    can_data = [0] * 8
    bms_data_settings_init()
    while True: 
        if GBT_Stage == GBT_STAGE.HANDSHAKE: 
            handleHandshake()
        elif GBT_Stage == GBT_STAGE.CONFIG:
            handleConfig()
        elif GBT_Stage == GBT_STAGE.CHARGING:
            pass
        elif GBT_Stage == GBT_STAGE.END:
            handleEnd()
        elif GBT_Stage == GBT_STAGE.ERRORS:
            handleError()
        else:
            break
    pass