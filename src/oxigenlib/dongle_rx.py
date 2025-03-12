"""
dongle_rx.py
------------
Decode and expose messages from the dongle
"""
from pydantic import BaseModel
from struct import unpack

class BytesLengthError(Exception):
    pass

class DongleRxData(BaseModel):
    status: int
    id: int
    last_lap_time_s: float
    lap_count: int
    power: int
    firmware: int
    buttons: int
    timestamp_msg_cs: int


def read_dongle_pkg(byte_package: bytes) -> DongleRxData:
    """ Decode 13bytes long messages (standard race state messages)
    from the dongle"""
    if len(byte_package) != 13:
        raise BytesLengthError
    status_byte, id_byte, last_lap_time_h, last_lap_time_l, lap_time_delay, lap_count_l, lap_count_h, \
         power_byte, firmware_byte, buttons_byte, timer_h, timer_m, timer_l = \
         unpack('13B', byte_package)

    return DongleRxData(
        status = status_byte,
        id = id_byte,
        last_lap_time_s = (last_lap_time_h * 256 + last_lap_time_l)/99.25,
        lap_count = lap_count_h*256 + lap_count_l,
        power = power_byte,
        firmware = firmware_byte,
        buttons = buttons_byte,
        timestamp_msg_cs = timer_h * 65536 + timer_m * 256 + timer_l - lap_time_delay
    )


class DongleRxFirmware(BaseModel):
    fw_major: int
    fw_minor: int

def read_dongle_firmware(byte_package: bytes) -> DongleRxFirmware:
    """ Decode 5bytes long messages (standard firmware version messages)
    from the dongle"""
    if len(byte_package) != 5:
        raise BytesLengthError
    fw_major, fw_minor, _1, _2, _3 = unpack('5B', byte_package)
    return DongleRxFirmware(
        fw_major=fw_major,
        fw_minor=fw_minor
    )
