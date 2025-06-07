"""
Constants Module
----------------
File: ``constants.py``

collection of important values for the oxigen protocol
"""
## trasmitting contants flags
# status byte
STATUS_RACE_MASK = 0x1F # b'0001 1111'
STATUS_PIT_LANE_LAP_TRIGGER_MASK = 0x20 # b'0010 0000'
STATUS_PIT_LANE_LAP_COUNT_MASK = 0x40 # b'0100 0000'
# command byte
COMMAND_MASK = 0x7F  # b'0111 1111'
GLOBAL_COMMAND_MASK = 0x80 # b'1000 0000'

POWER_TRIGGER_VALUE_MASK = 0x80  # b'1000 0000'

## receiving constants flags
# status byte
CAR_RESET_MASK = 0x01  # b'0000 0001'
CAR_ONLINE_MASK = 0x02  # b'0000 0010'
CAR_IN_PIT_LANE_MASK = 0x10  # b'0001 0000'
# power byte
POWER_MEAN_VALUE_MASK = 0x7F  # b'0111 1111'
CAR_ON_TRACK_MASK = 0x80  # b'1000 0000'
# firmware byte
MAIN_SW_RELEASE_MASK = 0x1F # b'0001 1111'
SUB_SW_RELEASE_MASK = 0x60 # b'0110 0000'
DEVICE_FW_MASK = 0x80 # b'1000 0000'
# buttons byte
BATT_LOW_MASK = 0x04 # b'0000 0100'
TRACK_CALL_MASK = 0x08 # b'0000 1000'
LAP_INFO_MASK = 0x10 # b'0001 0000'
BTN_UP_MASK = 0x20 # b'0010 0000'
BTN_DOWN_MASK = 0x40 # b'0100 0000'
BTN_ROUND_MASK = 0x80  # b'1000 0000'


