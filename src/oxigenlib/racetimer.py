"""
racetimer.py
------------
Simple Timer for providing a time reference in the messages to the dongle
"""
from time import monotonic_ns
from struct import pack

__all__ = ['RaceTimer']

class RaceTimer:
    def __init__(self):
        self._starting_time = 0
        self._paused_time = 0
        self._stopped_time = 0
        self._running = False

    def start(self):
        if not self._running:
            self._stopped_time = 0
            self._starting_time = monotonic_ns()
            self._running = True

    def pause(self):
        if self._running:
            self._paused_time = (monotonic_ns() - self._starting_time) + self._paused_time
            self._stopped_time = self._paused_time
            self._running = False

    def resume(self):
        if self._paused_time != 0:
            self.start()

    def stop(self):
        if self._running:
            self._stopped_time = (monotonic_ns() - self._starting_time) + self._paused_time
            self._paused_time = 0
            self._running = False

    def value(self):
        if self._running:
            return (monotonic_ns() - self._starting_time) + self._paused_time
        else:
            return self._stopped_time

    def value_cs(self):
        return self.value() // 10**7

    def value_cs_bytes(self):
        time = self.value_cs()
        # convert to 4 bytes with pack and straight to int with list
        bytes_list = list(pack('>i', time))
        # return only 3 bytes as oxigen protocol count time as 24bits int
        # skip the hoghest one
        return bytes_list[1:]

