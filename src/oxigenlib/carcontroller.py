"""
carcontroller.py
----------------
Convert data from dongle in a easy class CarState
"""
from pydantic import BaseModel, Field

from . import constants as o2
from .dongle_rx import DongleRxData

__all__ = ['CarController', 'decode_dongle_pkg']

class CarController(BaseModel):
    # from status byte
    car_reset: bool
    car_controller_link: bool
    car_in_pit_lane: bool
    # from id byte
    id: int =  Field(default_factory=int, ge=0, le=20)
    # from last_lap_time_* bytes
    last_lap_time_s: float =  Field(default_factory=float, ge=0)
    # from lap_count_* bytes
    lap_count: int = Field(default_factory=int, ge=0)
    # from power_byte byte
    power_mean_value: float =  Field(default_factory=float, ge=0)
    car_on_track: bool
    #  from firmware byte
    car_firmware: str
    controller_firmware: str
    # from buttons byte
    controller_batt_low: bool
    track_call_check: bool
    lap_time_info: bool
    arrow_up_btn: bool
    arrow_down_btn: bool
    round_btn: bool
    # from timer_* & lap_time_delay bytes
    timestamp_msg_cs: int = Field(default_factory=int, ge=0)


def decode_dongle_pkg(data: DongleRxData) -> CarController:
    """"""

    return CarController(
        # from status byte
        car_reset =(data.status & o2.CAR_RESET_MASK) == o2.CAR_RESET_MASK,
        car_controller_link = (data.status & o2.CAR_ONLINE_MASK) == o2.CAR_ONLINE_MASK,
        car_in_pit_lane  = (data.status & o2.CAR_IN_PIT_LANE_MASK) == o2.CAR_IN_PIT_LANE_MASK,
        # from id byte
        id = data.id,
        # from last_lap_time_* bytes
        last_lap_time_s = data.last_lap_time_s,
        # from lap_count_* bytes
        lap_count = data.lap_count,
        # from power_byte byte
        power_mean_value = (data.power & o2.POWER_MEAN_VALUE_MASK) / 127 * 10,
        car_on_track = (data.power & o2.CAR_ON_TRACK_MASK) == o2.CAR_ON_TRACK_MASK,
        # from firmware byte
        car_firmware = "unknown", # TODO
        controller_firmware = "unknown", # TODO
        # from buttons byte
        controller_batt_low = (data.buttons & o2.BATT_LOW_MASK) == o2.BATT_LOW_MASK,
        track_call_check = (data.buttons & o2.TRACK_CALL_MASK) == o2.TRACK_CALL_MASK,
        lap_time_info = (data.buttons & o2.LAP_INFO_MASK) == o2.LAP_INFO_MASK,
        arrow_up_btn = (data.buttons & o2.BTN_UP_MASK) == o2.BTN_UP_MASK,
        arrow_down_btn = (data.buttons & o2.BTN_DOWN_MASK) == o2.BTN_DOWN_MASK,
        round_btn = (data.buttons & o2.BTN_ROUND_MASK) == o2.BTN_ROUND_MASK,
        # from timer_* & lap_time_delay bytes
        timestamp_msg_cs = data.timestamp_msg_cs
    )
