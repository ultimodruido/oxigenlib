"""
utils.py
---------
collection of functions to send instruction via dongle
"""
from .config import O2Command, O2RaceStatus, O2Config, OxigenSystem
from .config import PitLaneTrigger, PitLaneCount, PowerMeanValue
from .config import RaceState, Command
from .racetimer import RaceTimer
from .dongle_tx import encode_race_status, encode_command
from .events import oxigen_events as events
__all__ = [
    'set_start_config',
    'set_system_max_speed',
    'set_race_state',
    'set_pit_stop_speed_limit',
    'set_car_max_speed',
    'set_car_min_speed',
    'set_car_max_brake'
]

# transmit_command_event = Signal(bytes)

def set_start_config(
        max_speed: int,
        pit_lane_trigger: PitLaneTrigger,
        pit_lane_count: PitLaneCount,
        power_mean_value: PowerMeanValue
) -> OxigenSystem:

    rs = O2RaceStatus(
        race_status=RaceState.STOPPED,
        max_speed=max_speed,
    )
    cfg = O2Config(
        pit_lane_trigger=pit_lane_trigger,
        pit_lane_count=pit_lane_count,
        power_mean_value=power_mean_value
    )
    return OxigenSystem(
        race_state=rs,
        config=cfg
    )


def set_system_max_speed(max_speed: int, sys: OxigenSystem, timer: RaceTimer) -> None:
    sys.race_state.max_speed = max_speed
    data = encode_race_status(race=sys.race_state, cfg=sys.config, ts=timer)
    events.transmit_command_event.emit(data)


def set_race_state(new_state: RaceState, sys: OxigenSystem, timer: RaceTimer):
    sys.race_state.race_status =new_state
    data = encode_race_status(race=sys.race_state, cfg=sys.config, ts=timer)
    events.transmit_command_event.emit(data)

def set_pit_stop_speed_limit(pit_speed: int, car_id: int, sys: OxigenSystem, timer: RaceTimer):
    cmd = O2Command(
        id=car_id,
        command=Command.SET_PIT_LANE_SPEED,
        command_arg=pit_speed
    )

    data = encode_command(race=sys.race_state, cfg=sys.config, cmd=cmd, ts=timer)
    events.transmit_command_event.emit(data)

def set_car_max_speed(max_speed: int, car_id: int, sys: OxigenSystem, timer: RaceTimer):
    cmd = O2Command(
        id=car_id,
        command=Command.SET_MAX_SPEED,
        command_arg=max_speed
    )

    data = encode_command(race=sys.race_state, cfg=sys.config, cmd=cmd, ts=timer)
    events.transmit_command_event.emit(data)

def set_car_min_speed(min_speed: int, car_id: int, sys: OxigenSystem, timer: RaceTimer):
    cmd = O2Command(
        id=car_id,
        command=Command.SET_MIN_SPEED,
        command_arg=min_speed
    )

    data = encode_command(race=sys.race_state, cfg=sys.config, cmd=cmd, ts=timer)
    events.transmit_command_event.emit(data)

def set_car_max_brake(max_brake: int, car_id: int, sys: OxigenSystem, timer: RaceTimer):
    cmd = O2Command(
        id=car_id,
        command=Command.SET_MAX_BRAKE,
        command_arg=max_brake
    )

    data = encode_command(race=sys.race_state, cfg=sys.config, cmd=cmd, ts=timer)
    events.transmit_command_event.emit(data)
