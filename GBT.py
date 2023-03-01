from structure import GBT_STAGE, charger_info_t
GBT_Stage = GBT_STAGE.HANDSHAKE
charger_info = charger_info_t()


def handleHandshake():
    pass
def GBTask():
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