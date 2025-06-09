"""
Dongle Module
-------------
File: ``dongle.py``

class and instance to communicate with the dongle
"""
import serial

from .dongle_rx import read_dongle_pkg, read_dongle_firmware
from .dongle_tx import encode_firmware_version_request, encode_free_race
from .events import oxigen_events as events

class Dongle:
    def __init__(self):
        self._port = ""
        self._dongle = None
        self._connected = False

    def connect(self, port: str) -> None:
        if self._connected:
            print(f"Dongle on port {self._port} is already connected. Try disconnecting first")
            return
        try:
            self._dongle = serial.Serial(port)
            self._connected = True
            # send firmware request
            data = encode_firmware_version_request()
            self.send(data)
            # read reply
            #data = read_dongle_firmware(self._dongle.read(5))
            _ = read_dongle_firmware(self._dongle.read(5))
            # TODO check that firmware is OK with this library
            # send free race so that the controller start notify themselves
            data = encode_free_race()
            self.send(data)
            # inform that connection was successful
            events.dongle_connected_event.emit(True)

        except serial.SerialException:
            print(f"Unable to open communication with the dongle on {port}. Try again")
            events.dongle_connected_event.emit(False)


    def send(self, bytes_data: bytes) -> None:
        if self._connected:
            self._dongle.write(bytes_data)
        else:
            events.dongle_connected_event.emit(False)

    def read(self) -> None:
        if self._connected:
            """Read a chunk of 13 bytes"""
            data = read_dongle_pkg(self._dongle.read(13))
            events.dongle_new_data_available_event.emit(data)
        else:
            events.dongle_connected_event.emit(False)


    def _flush(self, num_bytes: int) -> None:
        self._dongle.read(num_bytes)

    def check_data_waiting(self) -> None:
        if self._connected:
            bytes_in_pipeline = self._dongle.inWaiting()
            # check if waiting pipeline matches the expectation
            if (bytes_in_pipeline % 13) == 0:
                # read in chunks of 13 bytes
                self.read()
            else:
                # something went wrong -> flush the content of the pipeline
                self._flush(bytes_in_pipeline)
                events.dongle_flush_cache.emit()

oxigen_dongle = Dongle()


@events.transmit_command_event.connect
def _send(bytes_data: bytes) -> None:
    # forward signal to the class instance
    oxigen_dongle.send(bytes_data)
