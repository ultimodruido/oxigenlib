"""
OxigenLib
---------
TODO: add description
"""
VERSION = "0.1"

from .config import RaceState, Command, PitLaneTrigger, PitLaneCount, PowerMeanValue
from .config import O2Config, O2RaceStatus, OxigenSystem
from .events import oxigen_events as events
from .racers import oxigen_racers as racers
from .dongle import oxigen_dongle as dongle
from .racetimer import RaceTimer
from .utils import set_race_state


