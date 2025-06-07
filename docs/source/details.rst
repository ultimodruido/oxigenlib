Advanced Usage
==============
The script presented in getting started is is working but somehow limiting, in this section

Events
------

The library exposes the class Events as ``events`` instance variable.
All available events are attributes of the events instance. To link an event ''Signal'' to a slot::

    import oxigenlib as o2
    ...
    @o2.events.new_lap_event.connect
    def do_something(*args):
        print(args)



**List of available events:**

.. note::
    The library does not implement yet all the event that oxigen protocol identifies.
    Extension of events is planned for future releases

| ``new_lap_event(int, int, int, float, bool)`` raised when new lap event occur
|     parameters: [car id / car_laps_count / timestamp in centiseconds / laptime in seconds / info_flag]
|
| ``pit_lane_enter_event(int, int)`` raised when a car enter the pit lane
|     parameters: [car id / timestamp in centiseconds]
|
| ``pit_lane_leave_event(int, int)`` raised when a car leaves the pit lane
|     parameters: [car id / timestamp in centiseconds]
|
| ``track_call_event(bool, list)`` track button was pressed
|     parameters: [flag true-false / list of car ids with track call button pressed]
|
| ``all_cars_on_track_event(bool, list)`` flag raised when at least one car deslotted or when all cars are back on track
|     parameters: [flag true-false / list of car ids off-track]


The following events are also available but created for internal used. Only for *advanced* users.

| ``dongle_flush_cache()``
|     parameters: n/a
|
| ``dongle_connected_event(bool)`` raised after a connect attempt, returns the result of the connection attempt
|     parameters: [flag true-false]
|
| ``transmit_command_event(bytes)`` data ready to be sent to the dongle, payload attached
|     parameters: [bytes with data payload]
|
| ``dongle_new_data_available_event(DongleRxData)`` data package received from the dongle, the payload is already converted into a DongleRxData class
|     parameters: [DongleRxData]


Utilities
---------

Utility functions are available to send specific commands to the dongle, all functions are accessible
for simplificity are directly available in the oxigenlib name space.

So for example the ``set_system_max_speed`` utility function can be called as follows::

    import oxigenlib as o2
    ...
    o2.set_system_max_speed(max_speed, system, timer)



**Initial config**

``set_start_config`` is the starting point, it creates an ``OxigenSystem`` configuration:

.. autofunction:: oxigenlib.set_start_config

it returns a ``OxigenSystem`` class:

.. autoclass:: oxigenlib.OxigenSystem

**Race state management**

to control the race state (example stopped/paused/running/flagged) the following function comes handy.
refer to ``RaceState`` enumeration for available options.

.. autofunction:: oxigenlib.set_race_state

**Car controls**

The following set of functions enable the configuration of various car parameters during the race.

.. autofunction:: oxigenlib.set_system_max_speed
.. autofunction:: oxigenlib.set_car_max_speed
.. autofunction:: oxigenlib.set_car_min_speed
.. autofunction:: oxigenlib.set_pit_stop_speed_limit
.. autofunction:: oxigenlib.set_car_max_brake

Player
------

An additional function is available to get all details available for a specific id:

.. autofunction:: oxigenlib.get_player_data

If available the retrieved data is a ``CarController`` class:

.. autoclass:: oxigenlib.carcontroller.CarController


Timer
-----

Oxigen requires an external timebase, which has to be passed.
The library offers a simple timer implementation, but it may be easily replace by a self made implementation.


.. autoclass:: oxigenlib.racetimer.RaceTimer
    :members:

Important constants
-------------------

The following preset enumeration allow for a fast selection of important parameters:

.. autoclass:: oxigenlib.RaceState
   :members:
   :undoc-members:

.. autoclass:: oxigenlib.Command
   :members:
   :undoc-members:

.. autoclass:: oxigenlib.PitLaneTrigger
   :members:
   :undoc-members:

.. autoclass:: oxigenlib.PitLaneCount
   :members:
   :undoc-members:

.. autoclass:: oxigenlib.PowerMeanValue
   :members:
   :undoc-members:
