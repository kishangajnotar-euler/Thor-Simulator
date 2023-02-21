Sizeof_C1_F0 = 100 #not used
Sizeof_C1_F1 = 100 #not used

rx_RFID1_s = 0x120 #not used
rx_RFID2_s = 0x121 #not used
rx_RFID3_s = 0x122 #not used
rx_RFID4_s = 0x123 #not used
rx_RFID5_s = 0x124 #not used

rx_Modify_Settings_of_Board_s = 0x700 #not used

tx_stark       = 0x501
tx_6k6_charger = 0x1806E5F4
rx_6k6_charger = 0x18FF50E5

rx_FC_status = 0x72C
FC_ID        = 0x2C
tx_NMT_Start = 0x00
tx_Sync      = 0x80
tx_RPDO1     = 0x22C
tx_RPDO2     = 0x32C
rx_TPDO1     = 0x1AC

rx_BMS_01    = 0x101 #not used
rx_BMS_02    = 0x102 #not used
rx_BMS_10    = 0x110 #not used
rx_BMS_11    = 0x111
rx_BMS_12    = 0x112 #not used
rx_VID_502	 = 0x502
rx_VID_503	 = 0x503
rx_BMS_CHRGR = 0x1806E5F4  #NEW ID from BMS

#Cluser Data Parameters
rx_Screen_id       = 0x401
rx_energy_consumed = 0x402
rx_bill_param      = 0x403
rx_calander_param  = 0x404
rx_username_lower  = 0x405
rx_username_upper  = 0x406
rx_bill_amount     = 0x407

BaseAddressofRFIDdata = 0x120 #not used
EndAddressofRFIDdata  = 0x1FF #not used

rx_CHARGER_e_offset = 0 #not used

tx_CHARGER_s = 0x116 #not used

rx_BackendSYNC = 0x300 #not used
rx_SlowCharger = 0x18FF50E5
rx_FastCharger = 0x72C #not used