"""
OxigenLib
---------
TODO: add description
"""
#__all__ = ['oxigen_constants', 'utils']
#from .dongle import Dongle

from .config import RaceState, Command, PitLaneTrigger, PitLaneCount, PowerMeanValue
from .events import oxigen_events as events
from .racers import oxigen_racers as racers
from .dongle import oxigen_dongle as dongle
from .utils import set_race_state

