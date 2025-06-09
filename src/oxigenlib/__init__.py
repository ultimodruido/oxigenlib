"""
OxigenLib
---------
TODO: add description
"""
VERSION = "0.1"

from .config import RaceState, Command, PitLaneTrigger, PitLaneCount, PowerMeanValue
from .config import OxigenSystem
from .events import oxigen_events as events
from .dongle import oxigen_dongle as dongle
from .racetimer import RaceTimer
from .racers import *
from .utils import *


