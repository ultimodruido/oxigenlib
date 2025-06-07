"""
config.py
---------
collection of classes necessary to configure the system and enumeration types for confortable selection of the options
"""
from enum import Enum
from pydantic import BaseModel, Field
from .constants import STATUS_PIT_LANE_LAP_TRIGGER_MASK, STATUS_PIT_LANE_LAP_COUNT_MASK, POWER_TRIGGER_VALUE_MASK


__all__ = ['O2Config', 'O2RaceStatus', 'O2Command', 'OxigenSystem',
           'RaceState', 'Command', 'PitLaneCount', 'PitLaneTrigger', 'PowerMeanValue']


class RaceState(Enum):
    STOPPED = 0x01
    RUNNING = 0x03
    PAUSED = 0x04
    FLAGGED_LC_ON = 0x05
    FLAGGED_LC_OFF = 0x15


class Command(Enum):
    NO_ACTION = 0b00000000
    SET_PIT_LANE_SPEED = 0b00000001
    SET_MAX_SPEED = 0b00000010
    SET_MIN_SPEED = 0b00000011
    SET_RF_TX_LEV = 0b00000100
    SET_MAX_BRAKE = 0b00000101
    SET_MIN_LAP_TME = 0b00000111


class PitLaneTrigger(Enum):
    ENTER = 0x00
    LEAVE = STATUS_PIT_LANE_LAP_TRIGGER_MASK


class PitLaneCount(Enum):
    YES = 0x00
    NO = STATUS_PIT_LANE_LAP_COUNT_MASK


class PowerMeanValue(Enum):
    TRIGGER = 0
    PWM = POWER_TRIGGER_VALUE_MASK


class O2Config(BaseModel):
    pit_lane_trigger: PitLaneTrigger
    pit_lane_count: PitLaneCount
    power_mean_value: PowerMeanValue


class O2RaceStatus(BaseModel):
    race_status: RaceState
    max_speed: int = Field(default_factory=int, ge=0, le=255)


class O2Command(BaseModel):
    id: int = Field(default_factory=int, ge=0, le=20)
    command: Command
    command_arg: int


# TODO is OxigenSystem necessary?
class OxigenSystem(BaseModel):
    """
    Class representing an Oxigen system
    it has 2 attributes:

    :param race_state: class containing the actual race state, refer to the RaceState enum for options
    :type race_state: O2RaceStatus

    :param config: flag reminder if a car has recently been reset
    :type config: O2Config
    """
    race_state: O2RaceStatus
    config: O2Config
