"""
events.py
---------
central point for all internal and external events
"""
from psygnal import Signal

from .dongle_rx import DongleRxData


class Events:

    # dongle events
    dongle_connected_event = Signal(bool)
    # info new data available ready for transmission
    transmit_command_event = Signal(bytes)
    # new data arrived from the dongle
    dongle_new_data_available_event = Signal(DongleRxData)
    # dongle wrong cache length - need flush
    dongle_flush_cache = Signal()

    # module events
    # new lap event : id / timestamp / laptime / info_flag
    new_lap_event = Signal(int, int, float, bool)
    # pit enter-leave : event id / timestamp
    pit_lane_enter_event = Signal(int, int)
    pit_lane_leave_event = Signal(int, int)
    # global event
    track_call_event = Signal(bool)
    all_cars_on_track_event = Signal(bool)

oxigen_events = Events()
