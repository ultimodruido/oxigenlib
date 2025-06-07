"""
Racer Module
------------
File: ``racers.py``

Maintain and update the list of players.
This module exposes an instance of class ``Racers`` as ``oxigen_racers``.

"""
from typing import Optional
from pydantic import BaseModel

from .carcontroller import CarController, decode_dongle_pkg, create_new_player
from .dongle_rx import DongleRxData
from .events import oxigen_events as events


__all__ = ['get_player_data']

class Racers(BaseModel):
    """
    Container class for the data package returned by the dongle that represents car-controller pair

    ...

    Attributes
    ----------
    players: dict[int, CarController]
        dictionary of players/cars indexed by car id

    """
    players: dict[int, CarController]

    def update(self, data: DongleRxData) -> None:
        """
        update players info with new data arriving from the dongle

        :param data: class containing the received bytes from the dongle
        :type data: DongleRxData

        :return: None
        """
        # decode DongleRxData
        new_car_data = decode_dongle_pkg(data)
        # extract id
        car_id = new_car_data.id
        # compare differences

        # check if player exists:
        if car_id not in self.players.keys():
            self.players[car_id] = create_new_player(car_id)

        # check new lap
        if self.players[car_id].lap_count < new_car_data.lap_count:
            events.new_lap_event.emit(
                car_id,
                new_car_data.lap_count,
                new_car_data.timestamp_msg_cs,
                new_car_data.last_lap_time_s,
                new_car_data.lap_time_info
            )
        # check pit lanes
        if self.players[car_id].car_in_pit_lane != new_car_data.car_in_pit_lane:
            if new_car_data.car_in_pit_lane:
                events.pit_lane_enter_event.emit(car_id, new_car_data.timestamp_msg_cs)
            else:
                events.pit_lane_leave_event.emit(car_id, new_car_data.timestamp_msg_cs)


        # store new ca data in players list
        self.players[car_id] = new_car_data
        self.global_events_check()

    def global_events_check(self) -> None:
        """
        verify changes in global event and raise one if the case

        :return: None
        """
        # check for track call
        check_data = [(car.id, car.track_call_check, car.car_on_track) for car in self.players.values()]
        track_call_with_id = [car[0] for car in check_data if car[1]]
        if len(track_call_with_id):
            events.track_call_event.emit(True, track_call_with_id)
        else:
            events.track_call_event.emit(False, [])

        # check if all cars are on track
        car_not_on_track_with_id = [car[0] for car in check_data if not car[2]]
        if len(car_not_on_track_with_id):
            events.all_cars_on_track_event.emit(False, car_not_on_track_with_id)
        else:
            events.all_cars_on_track_event.emit(True, [])

    def get_player_data(self, player_id) -> Optional[CarController]:
        if player_id in self.players.keys():
            return self.players[player_id]
        else:
            return None

#empty_dict = {}
oxigen_racers = Racers(players={})

@events.dongle_new_data_available_event.connect
def _update(data: DongleRxData):
    # forward the signal to the class
    oxigen_racers.update(data)

def get_player_data(car_id: int) -> Optional[CarController]:
    """
    Retrieve all data available for a plyer/car.

    :param car_id: Number of the car to which the limitation applies
    :type car_id: int

    :return: None if no data is available or a ``CarController`` instance
    """
    oxigen_racers.get_player_data(car_id)