.. OxigenLib documentation master file, created by
   sphinx-quickstart on Fri May  9 23:09:12 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

OxigenLib
=========
OxigenLib is a python library which simplifies the interaction with the Slot.it Oxigen Dongle (NOTE: Version 4+)

Slot.it developed a wireless digital racing system for slot cars, called `Oxigen <https://slot.it/oxigen/>`_.
The dongle is a USB device that translates commands from a serial connection to wireless instruction for the
cars on the track.


.. warning::

   This project is under active development.

.. note::
   This library is not an RMS (race management system). It is intended as backend layer to be used by external RMS

OxigenLib is developed around a Signal/Slot implementation similar to `Qt GUI <https://doc.qt.io/qt-6/signalsandslots.html>`_
The existing python library `psygnal <https://pypi.org/project/psygnal/>`_ is used for this purpose.

If you want to start using OxigenLib, check the user guide :)

Features
--------

- focus on clean communication with dongle, expose data in class-organized format
- do not keep track of race information, this task is demanded to the RMS
- signal/slot messaging system (in Qt-style) to inform the RMS about changing in the car state
- include a simple timer for time alignment with the dongle (with optional timer value injection from RMS)



.. toctree::
   :maxdepth: 2
   :caption: User guide:

   intro

   details


.. toctree::
   :maxdepth: 2
   :caption: Developer interface:

   api
