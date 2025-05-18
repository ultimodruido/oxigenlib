"""
Racetimer Module
----------------
File: ``racetimer.py``

Simple Timer for providing a time reference in the messages to the dongle
TODO: extend using a Protocol to allow use of external provided timers
"""
from time import monotonic_ns
from struct import pack

__all__ = ['RaceTimer']

class RaceTimer:
    """
    Simple timer to control oxigen protocol base time reference. It can be substituted by another timer
    as long as it offers the same functions.
    """
    def __init__(self):
        self._starting_time = 0
        self._paused_time = 0
        self._stopped_time = 0
        self._running = False

    def start(self) -> None:
        """start counting time"""
        if not self._running:
            self._stopped_time = 0
            self._starting_time = monotonic_ns()
            self._running = True

    def pause(self) -> None:
        """pause counting time, but does not reset the timer value"""
        if self._running:
            self._paused_time = (monotonic_ns() - self._starting_time) + self._paused_time
            self._stopped_time = self._paused_time
            self._running = False

    def resume(self) -> None:
        """restart counting time, but does not reset the timer value"""
        if self._paused_time != 0:
            self.start()

    def stop(self) -> None:
        """stops the timer, but cannot be restartet, by new start the counter restart from zero"""
        if self._running:
            self._stopped_time = (monotonic_ns() - self._starting_time) + self._paused_time
            self._paused_time = 0
            self._running = False

    def value(self) -> int:
        """return timer counter in system timebase [ns]"""
        if self._running:
            return (monotonic_ns() - self._starting_time) + self._paused_time
        else:
            return self._stopped_time

    def value_cs(self) -> int:
        """return timer counter in centiseconds [cs] timebase -> used by oxigen"""
        return self.value() // 10**7

    def value_cs_bytes(self) -> list[int]:
        """return the timer counter in [cs] base as a 4 bytes list, used for the transmission to the dongle"""
        time = self.value_cs()
        # convert to 4 bytes with pack and straight to int with list
        bytes_list = list(pack('>i', time))
        # return only 3 bytes as oxigen protocol count time as 24bits int
        # skip the hoghest one
        return bytes_list[1:]
