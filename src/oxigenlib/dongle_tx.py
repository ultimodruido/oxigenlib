"""
dongle_tx.py
------------
Decode and send messages from the dongle
"""
from struct import pack

#from . import config
#from . import constants as o2
from .racetimer import RaceTimer
from .config import O2Config, O2RaceStatus, O2Command, Command

# TODO: protocols?!
#__all__ = ['encode_race_status', 'encode_command']

def encode_race_status(race: O2RaceStatus, cfg: O2Config, ts: RaceTimer) -> bytes:
    # TODO: coupling! how to access value better?
    byte0 = race.race_status.value | cfg.pit_lane_count.value | cfg.pit_lane_trigger.value
    byte1 = race.max_speed
    byte2 = 0x00 # controller ID
    byte3 = 0x00 # global command
    byte4 = 0x00 # command argument
    byte5 = 0x80 # car command / no command
    byte6 = 0x00 # command argument
    byte7 = cfg.power_mean_value.value

    # race start
    return pack('11B', byte0, byte1, byte2, byte3, byte4, byte5, byte6, byte7, *ts.value_cs_bytes())


def _encode_global_command(race: O2RaceStatus, cfg: O2Config, cmd: O2Command, ts: RaceTimer) -> bytes:
    byte0 = 0x06 | cfg.pit_lane_count.value | cfg.pit_lane_trigger.value
    byte1 = race.max_speed
    byte2 = 0x00  # controllder ID
    byte3 = cmd.command.value # global command
    byte4 = cmd.command_arg  # command argument
    byte5 = 0x80 | Command.NO_ACTION.value  # car command / no action
    byte6 = 0x00  # command argument
    byte7 = cfg.power_mean_value.value

    # race start
    return pack('11B', byte0, byte1, byte2, byte3, byte4, byte5, byte6, byte7, *ts.value_cs_bytes())


def _encode_car_command(race: O2RaceStatus, cfg: O2Config, cmd: O2Command, ts: RaceTimer) -> bytes:
    byte0 = 0x06 | cfg.pit_lane_count.value | cfg.pit_lane_trigger.value
    byte1 = race.max_speed
    byte2 = cmd.id  # controllder ID
    byte3 = Command.NO_ACTION.value  # global command / no action
    byte4 = 0x00 # command argument
    byte5 = 0x80 | cmd.command.value  # car command
    byte6 = cmd.command_arg  # command argument
    byte7 = cfg.power_mean_value.value

    # race start
    return pack('11B', byte0, byte1, byte2, byte3, byte4, byte5, byte6, byte7, *ts.value_cs_bytes())

def encode_command(race: O2RaceStatus, cfg: O2Config, cmd: O2Command, ts: RaceTimer) -> bytes:
    if cmd.id == 0:  # global command
        return _encode_global_command(race, cfg, cmd, ts)
    else:  # car specific command
        return _encode_car_command(race, cfg, cmd, ts)

def encode_firmware_version_request() -> bytes:
    return pack('11B', 0x06, 0x06, 0x06, 0x06, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00)

def encode_free_race() -> bytes:
    return pack('11B', 0x0F, 0xFF, 0x00, 0x00, 0x00, 0x80, 0x00, 0x80, 0x00, 0x00, 0x00)
