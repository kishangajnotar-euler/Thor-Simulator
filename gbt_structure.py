from typing import Union
from enum import Enum
class bro_data_t():
    bro_reasult=0
bro_data=bro_data_t()

class cro_data_t():
    cro_reasult=0
cro_data=cro_data_t()

class chm_data_t():
    def __init__(self):
        self.version_1 = 0
        self.version_0 = 0
chm_data=chm_data_t()

class crm_data_t:
    def __init__(self):
        self.crm_result = 0
        self.charger_sn = 0
crm_data=crm_data_t()

class cts_data_t:
    def __init__(self):
        self.S = 0
        self.M = 0
        self.H = 0
        self.d = 0
        self.m = 0
        self.Y = 0
cts_data=cts_data_t()

class cml_data_t:
    def __init__(self):
        self.max_output_voltage = 0
        self.min_output_voltage = 0
        self.max_output_current = 0
        self.min_output_current = 0
cml_data=cml_data_t()

class ccs_data_t:    # Not right correct this 
    def __init__(self):
        self.output_voltage = 0
        self.output_current = 0
        self.total_charge_time = 0
        self.charge_enable = 0
ccs_data=ccs_data_t()

class cst_data_t:
    def __init__(self):
        self.stop_reason_condition = 0
        self.stop_reason_manual = 0
        self.stop_reason_fault = 0
        self.stop_reason_bms_stop = 0
        self.stop_fault_reason_temperature = 0
        self.stop_fault_reason_connector = 0
        self.stop_fault_reason_inner_temperature = 0
        self.stop_fault_reason_charge = 0
        self.stop_fault_reason_emergency = 0
        self.stop_fault_reason_other = 0
        self.stop_error_reason_current = 0
        self.stop_error_reason_voltage = 0
cst_data=cst_data_t()

class csd_data_t:
    def __init__(self):
        self.total_charge_time = 0
        self.total_charge_energy = 0
        self.charger_sn = 0
csd_data=csd_data_t()

class cem_data_t:
    def __init__(self):
        self.brm_timeout = 0
cem_data=cem_data_t()


class bms_data_settings_t:
    def __init__(self):
        self.dst = 0
        self.src = 0
        self.chm_data = chm_data_t()
        self.crm_data = crm_data_t()
        self.cts_data = cts_data_t()
        self.cml_data = cml_data_t()
        self.ccs_data = ccs_data_t()
        self.cst_data = cst_data_t()
        self.csd_data = csd_data_t()
        self.cem_data = cem_data_t()
settings=bms_data_settings_t()

class brm_data_t:
    def __init__(self) -> None:
        self.version_1 = 0x01
        self.version_0 = 0x01
        self.battery_type = 0x01
        self.total_battery_rate_capicity
        self.total_battery_rate_voltage
class bcl_data_t:
        def __init__(self) -> None:
            self.require_voltage = 0
            self.require_current = 0
            self.charge_mode = 0x01

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
        self.settings = bms_data_settings_t()
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

class bcs_data_t:
    def __init__(self):
        self.charge_voltage=0.1
        self.charge_current=0.1
        self.soc=0
        self.remain_min=0
class bsm_data_t:
    def __init__(self) :
        self.single_max_voltage_group=0
        self.battery_max_temperature=0
        self.battery_max_temperature_sn=0
        self.battery_min_temperature=0
        self.battery_min_temperature_sn=0
        
bcl_data = bcl_data_t()
bcs_data=bcs_data_t()
bsm_data=bsm_data_t()
brm_data = brm_data_t()
GBT_Stage = GBT_STAGE.HANDSHAKE
charger_info = charger_info_t()

class J1939_Message_t:
        def __init__(self):
            self.pgn = 0
            self.size = 0
            self.data = bytearray(1785)
mp_msg=J1939_Message_t()      