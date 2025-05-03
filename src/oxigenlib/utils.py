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
    """
    Set the initial configuration of the Oxigen system.

            Parameters:
                    max_speed (int): A decimal integer between 0 and 255
                    pit_lane_trigger (PitLaneTrigger): enum defining if the entering or leaving
                                                       the pitlane triggers also lane count
                    pit_lane_count (PitLaneCount): enum defining if the pitlane triggers also lane count
                    power_mean_value (PowerMeanValue): enum defining if the average trigger position
                                                       or the transferred PWM value is reported for fuel consumption

            Returns:
                    OxigenSystem: class descriptor of the system in use
    """
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
    """
    Set the maximum speed allowed.

            Parameters:
                    max_speed (int): A decimal integer between 0 and 255
                    sys (OxigenSystem): class describing the system configuration
                    timer (RaceTimer): class providing timer functions

            Returns:
                    None
    """
    sys.race_state.max_speed = max_speed
    data = encode_race_status(race=sys.race_state, cfg=sys.config, ts=timer)
    events.transmit_command_event.emit(data)


def set_race_state(new_state: RaceState, sys: OxigenSystem, timer: RaceTimer) -> None:
    """
    Set the race state.

            Parameters:
                    new_state (RaceState): enum defining the desired state to be applied to the race
                    sys (OxigenSystem): class describing the system configuration
                    timer (RaceTimer): class providing timer functions

            Returns:
                    None
    """
    sys.race_state.race_status =new_state
    data = encode_race_status(race=sys.race_state, cfg=sys.config, ts=timer)
    events.transmit_command_event.emit(data)

def set_pit_stop_speed_limit(pit_speed: int, car_id: int, sys: OxigenSystem, timer: RaceTimer) -> None:
    """
    Limit the maximum speed in pitlanes.

            Parameters:
                    pit_speed (int): A decimal integer between 0 and 255
                    car_id (int): Number of the car to which the limitation applies, if 0 applies to all cars
                    sys (OxigenSystem): class describing the system configuration
                    timer (RaceTimer): class providing timer functions

            Returns:
                    None
    """
    cmd = O2Command(
        id=car_id,
        command=Command.SET_PIT_LANE_SPEED,
        command_arg=pit_speed
    )

    data = encode_command(race=sys.race_state, cfg=sys.config, cmd=cmd, ts=timer)
    events.transmit_command_event.emit(data)

def set_car_max_speed(max_speed: int, car_id: int, sys: OxigenSystem, timer: RaceTimer) -> None:
    """
    Limit the maximum speed of a car.

            Parameters:
                    max_speed (int): A decimal integer between 0 and 255
                    car_id (int): Number of the car to which the limitation applies, if 0 applies to all cars
                    sys (OxigenSystem): class describing the system configuration
                    timer (RaceTimer): class providing timer functions

            Returns:
                    None
    """
    cmd = O2Command(
        id=car_id,
        command=Command.SET_MAX_SPEED,
        command_arg=max_speed
    )

    data = encode_command(race=sys.race_state, cfg=sys.config, cmd=cmd, ts=timer)
    events.transmit_command_event.emit(data)

def set_car_min_speed(min_speed: int, car_id: int, sys: OxigenSystem, timer: RaceTimer) -> None:
    """
    Limit the minimum speed of a car.

            Parameters:
                    min_speed (int): A decimal integer between 0 and 255
                    car_id (int): Number of the car to which the limitation applies, if 0 applies to all cars
                    sys (OxigenSystem): class describing the system configuration
                    timer (RaceTimer): class providing timer functions

            Returns:
                    None
    """
    cmd = O2Command(
        id=car_id,
        command=Command.SET_MIN_SPEED,
        command_arg=min_speed
    )

    data = encode_command(race=sys.race_state, cfg=sys.config, cmd=cmd, ts=timer)
    events.transmit_command_event.emit(data)

def set_car_max_brake(max_brake: int, car_id: int, sys: OxigenSystem, timer: RaceTimer) -> None:
    """
    Limit the brake force of a car.

            Parameters:
                    max_brake (int): A decimal integer between 0 and 255
                    car_id (int): Number of the car to which the limitation applies, if 0 applies to all cars
                    sys (OxigenSystem): class describing the system configuration
                    timer (RaceTimer): class providing timer functions

            Returns:
                    None
    """
    cmd = O2Command(
        id=car_id,
        command=Command.SET_MAX_BRAKE,
        command_arg=max_brake
    )

    data = encode_command(race=sys.race_state, cfg=sys.config, cmd=cmd, ts=timer)
    events.transmit_command_event.emit(data)
