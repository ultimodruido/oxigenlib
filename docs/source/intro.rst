Getting started
===============
This library is developed under the GPL v3 licence.

.. note::
   This library is not an RMS (race management system). It is intended as backend layer to be used by external RMS

This library is designed to implement the version 4.x of the Oxigen protocol.
The specification is available `here <https://slot.it/Download/oXigen/Manuals/PCDongleProtocol_v_4.06.pdf>`_

OxigenLib is developed around a Signal/Slot implementation similar to `Qt GUI <https://doc.qt.io/qt-6/signalsandslots.html>`_
The existing python library `psygnal <https://pypi.org/project/psygnal/>`_ is used for this purpose.


Necessary hardware
------------------
The only strictly necessary hardware is the Oxigen dongle (type O204b, the _blue_ version), but ti makes sense to have a couple
of chipped slot car too :P


How to use the library
----------------------
The library regularly checks for new transmission from the dongle on the serial port. As soon as new data are available
specific events are raised. To start using the library few steps are necessary:

* import the library
* configure the system (see the protocol description)
* init the timer
* connect to the events of interest
* init the dongle with the serial port to which it is connected
* loop regularly over the ``check_data_waiting`` method of the ``dongle`` instance

::

    # import the oxigen library
    import oxigenlib as o2

    # configure the system
    # example: pit lane does not trigger lane counter
    # PWM value used for fuel consumption
    # configure the system
    system = o2.set_start_config(
            max_speed = CAR_LIMIT_MAX_SPEED,
            pit_lane_trigger = o2.PitLaneTrigger.LEAVE,
            pit_lane_count = o2.PitLaneCount.NO,
            power_mean_value = o2.PowerMeanValue.PWM
    )

    # use internal timer for simplicity
    timer = o2.RaceTimer()
    timer.start()

    # catch the events
    # new lap
    @o2.events.new_lap_event.connect
    def lap(car_id, lap_count, timestamp, laptime, info_flag):
        print(f"ID{car_id}: new lap ({lap_count}) at {timestamp}cs")

    # safety car
    CAR_LIMIT_SAFETY_CAR_SPEED = 0x66 # or integer 102 so circa 40% of max speed
    @o2.events.all_cars_on_track_event.connect
    def all_cars_on_track(value, car_list):
        if value is False:
            print("EMERGENCY! SAFETY CAR OUT!")
            # action -> limit max speed for all cars
            o2.set_system_max_speed(CAR_LIMIT_SAFETY_CAR_SPEED, system, timer)
            # print list of car not on track
            for car_id in car_list:
                print(f"Car ID{car_id} had an accident!")
        else:
            # no emergency -> restore full speed
            o2.set_system_max_speed(CAR_LIMIT_MAX_SPEED, system, timer)

    # init and connect to the dongle
    o2.dongle.connect("COM8")

    #start the race
    o2.set_race_state(
        new_state=o2.RaceState.RUNNING,
        sys=system,
        timer=timer
    )

    # poll for new data in the dongle
    while True:
        o2.dongle.check_data_waiting()


Known bugs & TODO
-----------------

TODO improve recognition of dongle:
so far no check of protocol version, and error when the dongle was already initialized

TODO improve interface
may be change speed input to range 0-100% instead of binary values (0-255)


Examples
--------

TODO
show example of smartrace interface