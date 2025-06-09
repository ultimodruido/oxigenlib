# Oxigen python library
A simple generic library to interact with the oxigen dongle (version 4)

> [!WARNING]
> This project is in an embryonic stage. Function and class signatures are not stable

## Goals
Features in current plan:
- do not keep track of race information, this task is demanded to the RMS
- decode dongle protocol and expose a simple class with the received state of all data in a Car-Controller pair
- offer a signal/slot messaging system (in Qt-style) to inform the RMS about changing in the car state
- implement a simple timer for time alignment with the dongle (with optional timer value injection from RMS)

*Check the [latest doc on Read the Docs](https://oxigenlib.readthedocs.io/en/latest/)*