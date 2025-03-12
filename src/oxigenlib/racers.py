"""
racers.py
---------
maintain and update the list of players
"""
from pydantic import BaseModel

from .carcontroller import CarController, decode_dongle_pkg
from .dongle_rx import DongleRxData
from .events import oxigen_events as events


class Racers(BaseModel):
    players: dict[int, CarController]

    def update(self, data: DongleRxData):
        # TODO
        # decode DongleRxData
        new_car_data = decode_dongle_pkg(data)
        # extract id
        car_id = new_car_data.id
        # compare differences

        # check new lap
        if self.players[car_id].lap_count < new_car_data.lap_count:
            events.new_lap_event.emit(
                car_id,
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

    def global_events_check(self):
        # check for track call
        check_data = [car.track_call_check for car in self.players.values()]
        if any(check_data):
            events.track_call_event.emit(True)
        else:
            events.track_call_event.emit(False)

        # checl all cars on track
        check_data = [car.car_on_track for car in self.players.values()]
        if all(check_data):
            events.all_cars_on_track_event.emit(True)
        else:
            events.all_cars_on_track_event.emit(False)

#empty_dict = {}
oxigen_racers = Racers(players={})

@events.dongle_new_data_available_event.connect
def _update(data: DongleRxData):
    # forward the signal to the class
    oxigen_racers.update(data)