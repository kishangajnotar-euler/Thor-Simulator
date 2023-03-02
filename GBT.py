from main import GBT_Stage, charger_info
from structure import GBT_STAGE, crm_data_t, cml_data, bcl_data, crm_data
import time
from datetime import datetime, timedelta
from BMSdata import rxBMSData
from structure import GBT_STAGE, charger_info_t
import time
from gbt_structure import *
from main import CAN_1, CAN_2
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


def send_crm(can_data: list) -> None:
    can_data[0] = crm_data.crm_result & 0xFF
    can_data[1] = crm_data.charger_sn & 0xFF
    can_data[2] = 0x00 & 0xFF
    can_data[3] = 0x00 & 0xFF
    can_data[4] = 0x00 & 0xFF
    can_data[5] = 0x68 & 0xFF
    can_data[6] = 0x69 & 0xFF
    can_data[7] = 0x76 & 0xFF
    msg = can.Message(arbitration_id=canID.GBT_CRM_CAN_ID, data=can_data, is_extended_id=True)
    CAN_1.send(msg)


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

def prepare_state_css():
    charger_info.bsm_received = 0
def prepare_state_cst():
    charger_info.bsd_received = 0

def handleCharging(can_data):
    while (GBT_Stage == GBT_STAGE.CHARGING):
        if charger_info.bcl_received == 1:
            prepare_state_css()
            prepare_state_cst()
            while True:
                iSet = min(cml_data.max_output_current, bcl_data.require_current)
                vSet =  bcl_data.require_voltage
                iSet=iSet*10
                vSet=vSet*10
                rxBMSData[0] = vSet >> 8
                rxBMSData[1] = vSet & 0xFF
                rxBMSData[2] = iSet >> 8
                rxBMSData[3] = iSet & 0xFF
                msg = can.Message(arbitration_id=canID.GBT_CCS_CAN_ID, data=can_data, is_extended_id=True)
                CAN_1.send(msg)
                msg = can.Message(arbitration_id=canID.tx_6k6_charger, data=rxBMSData, is_extended_id=True)
                CAN_2.send(msg)

                time.sleep(0.05)

                if charger_info.bst_received == 1:
                    send_cst()
                    time.sleep(0.01)
                    GBT_Stage = GBT_STAGE.END
        else:
            send_cro()
            time.sleep(0.25)
    if GBT_Stage == GBT_STAGE.CHARGING:
        GBT_Stage = GBT_STAGE.END

def GBTask():
    bms_data_settings_init()
    can_data = [0] * 8

    cml_data.max_output_voltage = 1000.0
    cml_data.min_output_voltage = 500.0
    cml_data.max_output_current = 1200.0
    cml_data.min_output_current = 400

    while True: 
        if GBT_Stage == GBT_STAGE.HANDSHAKE: 
            handleHandshake()
        elif GBT_Stage == GBT_STAGE.CONFIG:
            handleConfig()
        elif GBT_Stage == GBT_STAGE.CHARGING:
            handleCharging(can_data)
            pass
        elif GBT_Stage == GBT_STAGE.END:
            pass
        elif GBT_Stage == GBT_STAGE.ERRORS:
            pass
        else:
            break
    pass