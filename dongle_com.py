"""
Decode and expose 13 byte long messages from the dongle
TODO: add also recognizion of firmware message from the dongle
"""
from dataclasses import dataclass
from struct import unpack

@dataclass
class DongleRxData:
    status: int
    id: int
    last_lap_time_s: float
    lap_count: int
    power: int
    firmware: int
    buttons: int
    timestamp_msg_cs: int


def read_dongle_pkg(byte_package):
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
