"""
Events Module
-------------
File: ``events.py``

Central point for all internal and external events. The event system is based on the module ``psygnal``,
importing this module exposes the variable ``oxigen_events`` which is an instance of ``Events`` class.
All events in OxigenLib are attributes of the class ``Events``.

Connection slot to event signals requires the connect decorator::

    @oxigen_events.new_lap_event.connect
    def lap(car_id, lap_count, timestamp, laptime, info_flag):
        print(f"ID{car_id}: new lap ({lap_count}) at {timestamp}cs")
        send_smartrace_fl(car_id, timestamp * 10)
"""
from psygnal import Signal

from .dongle_rx import DongleRxData


class Events:
    """
    Container class for all events in the library

    List of available events

    :var dongle_flush_cache: ``type: Signal()`` in case of misalignment in payload bytes, it can be used to flush the dongle cache
    :var new_lap_event: ``type: Signal(int, int, int, float, bool)`` raised when new lap event occur -> id / car_laps_count / timestamp [centiseconds] / laptime [seconds] / info_flag
    :var pit_lane_enter_event: ``type: Signal(int, int)`` raised when a car enter the pit lane -> car id / timestamp [centiseconds]
    :var pit_lane_leave_event: ``type: Signal(int, int)`` raised when a car leaves the pit lane -> car id / timestamp [centiseconds]
    :var track_call_event: ``type: Signal(bool, list)`` track button was pressed -> flag true-false / list of car ids with track call pressed
    :var all_cars_on_track_event: ``type: Signal(bool, list)`` flag raised when at least one car deslotted or when all cars are back on track -> flag true-false / list of car ids off-track

    The following events are also available but internally used. Only for advance users

    :var dongle_connected_event: ``type: Signal(bool_connecting_result)`` raised after a connect attempt, return the result of the connection attempt
    :var transmit_command_event: ``type: Signal(bytes_data_payload)`` data ready to be sent to the dongle, payload attached
    :var dongle_new_data_available_event: ``type: Signal(DongleRxData)`` data package received from the dongle, the payload is already converted into a DongleRxData class
    """

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
    new_lap_event = Signal(int, int, int, float, bool)
    # pit enter-leave : event id / timestamp
    pit_lane_enter_event = Signal(int, int)
    pit_lane_leave_event = Signal(int, int)
    # global event
    track_call_event = Signal(bool)
    all_cars_on_track_event = Signal(bool)

oxigen_events = Events()
