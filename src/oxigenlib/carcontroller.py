"""
CarController Module
--------------------
File: ``carcontroller.py``

This module provides a convenience class CarController to transfer the input data from the dongle to other users.
"""
from pydantic import BaseModel, Field

from . import constants as o2
from .dongle_rx import DongleRxData

__all__ = ['CarController', 'decode_dongle_pkg', 'create_new_player']

class CarController(BaseModel):
    """
    Container class for the data package returned by the dongle that represents car-controller pair

    :param car_reset: flag reminder if a car has recently been reset
    :type car_reset: bool
    :param car_controller_link: link to car available
    :type car_controller_link: bool
    :param car_in_pit_lane: flag if car is in the pitlane
    :type car_in_pit_lane: bool
    :param id: identification number of the car
    :type id: int
    :param last_lap_time_s: keep the last lap time in seconds
    :type last_lap_time_s: float
    :param lap_count: numbers of laps recorded by the car
    :type lap_count: int
    :param power_mean_value: position of trigger or average value of pwm signal.
        It depends on the configuration parameter of the system
    :type power_mean_value: float
    :param car_on_track: flag reporting if the car is or not on the track
    :type car_on_track: bool
    :param car_firmware: firmware value of car chip
    :type car_firmware: str
    :param controller_firmware: firmware value of the controller
    :type controller_firmware: str

    :param controller_batt_low: flag reporting low battery status
    :type controller_batt_low: bool
    :param track_call_check: flag reporting if controller reported track call
    :type track_call_check: bool

    :param lap_time_info: flag reporting if lap time includes a 'short lap'
    :type lap_time_info: bool
    :param arrow_up_btn: up button pressed on controller
    :type arrow_up_btn: bool
    :param arrow_down_btn: down button pressed on controller
    :type arrow_down_btn: bool
    :param round_btn: up button pressed on controller
    :type round_btn: bool

    :param timestamp_msg_cs: timestamp of the transmitted message in centiseconds.
        Value already aligned with the dongle timer according formula _race timer (last lap)_
        of the official oxigen documentation
    :type timestamp_msg_cs: int
    """
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
    """
    Convert dongle package into readable an structured CarController class

    :param data: class containing the received bytes from the dongle
    :type data: DongleRxData

    :return: content of dongle transmission converted in easy format into class CarController
    :rtype: CarController
    """

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


def create_new_player(car_id: int) -> CarController:
    """
    Support function to generate an empty CarController class for a new player with a known id.
    Useful to generate a starting CarController while filling the racers list at the registration fase

    :param car_id: Number of the car to add to the system
    :type car_id: int

    :return: content of dongle transmission converted in easy format into class CarController
    :rtype: CarController
    """

    return CarController(
        # from status byte
        car_reset = False,
        car_controller_link = True,
        car_in_pit_lane  = False,
        # from id byte
        id = car_id,
        # from last_lap_time_* bytes
        last_lap_time_s = 0,
        # from lap_count_* bytes
        lap_count = 0,
        # from power_byte byte
        power_mean_value = 0,
        car_on_track = True,
        # from firmware byte
        car_firmware = "unknown", # TODO
        controller_firmware = "unknown", # TODO
        # from buttons byte
        controller_batt_low = False,
        track_call_check = False,
        lap_time_info = False,
        arrow_up_btn = False,
        arrow_down_btn = False,
        round_btn = False,
        # from timer_* & lap_time_delay bytes
        timestamp_msg_cs = 0
    )