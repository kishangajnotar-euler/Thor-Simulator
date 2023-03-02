from typing import Union

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



 
# typedef  struct  { 
# 	union  { 
# 		struct  { 
# 			uint8_t  brm_timeout :  2  ;  //  0x00-normal, 0x01-timeout, 0x10-untrusted state 
# 			uint8_t  reserved_0 :  6 ; 
# 		} s; 
# 		uint8_t v  ; 
# } u1; 
# 	union  { 
# 		struct  { 
# 			uint8_t  bcp_timeout :  2  ;  //  0x00-normal, 0x01-timeout, 0x10-untrusted state 
# 			uint8_t  bro_timeout :  2  ;  //  0x00-normal, 0x01-timeout, 0x10-untrusted status 
# 			uint8_t  reserved_1 :  4 ; 
# 		} s; 
# 		uint8_t v  ; 
# } u2; 
# 	union  { 
# 		struct  { 
# 			uint8_t  bcs_timeout :  2  ;  //  0x00-normal, 0x01-timeout, 0x10-untrusted state 
# 			uint8_t  bcl_timeout :  2  ;  //  0x00-normal, 0x01-timeout, 0x10-untrusted state 
# 			uint8_t  bst_timeout :  2  ;  //  0x00-normal, 0x01-timeout, 0x10-untrusted state 
# 			uint8_t  reserved_2 :  2 ; 
# 		} s; 
# 		uint8_t v  ; 
# } u3; 
# 	union  { 
# 		struct  { 
# 			uint8_t  bsd_timeout :  2  ;  //  0x00-normal, 0x01-timeout, 0x10-untrusted state 
# 			uint8_t  other :  6 ; 
# 		} s; 
# 		uint8_t v  ; 
# } u4; 
# }  cem_data_t ; 