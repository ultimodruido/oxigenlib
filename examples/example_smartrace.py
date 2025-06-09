"""
Example for oxigenlib with smartrace
"""

import argparse

from time import sleep
from websockets.sync.client import connect

import oxigenlib as o2


CONTINUE_LOOP = True
# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("smartrace", help = "Smartrace Server -> example 192.158.16.24")
parser.add_argument("port", help = "Smartrace port -> example 50860")

parser.add_argument("dongle", help = "Dongle serial port -> example COM8")

parser.add_argument("-pe", "--pit_enter",
                    help = "add this flag if pit enter also  triggers lane count",
                    action="store_true")
parser.add_argument("-pl", "--pit_leave",
                    help = "add this flag if pit leave also  triggers lane count",
                    action="store_true")

parser.add_argument("-s", "--max_speed",
                    help = "set maximum speed [0-255]",
                    type=int,
                    default=255)

parser.add_argument("-sc", "--safety_car",
                    help = "set maximum speed if safety car is out [0-255]",
                    type=int,
                    default=255)

parser.add_argument("-ps", "--pit_speed",
                    help = "set maximum speed in pit lane [0-255]",
                    type=int,
                    default=255)


args = parser.parse_args()


CAR_LIMIT_MAX_SPEED = 0xFF
if args.max_speed:
    CAR_LIMIT_MAX_SPEED = args.max_speed

CAR_LIMIT_SAFETY_CAR_SPEED = 0xFF
if args.safety_car:
    CAR_LIMIT_SAFETY_CAR_SPEED = min(args.safety_car, CAR_LIMIT_MAX_SPEED)

# TODO: che only one -pe OR -pl


pit_trigger = o2.PitLaneTrigger.LEAVE
pit_count = o2.PitLaneCount.NO
if args.pit_enter and args.pit_leave:
    raise ValueError("pit_enter and pit_leave are mutually exclusive, use only one")

if args.pit_enter:
    pit_trigger = o2.PitLaneTrigger.ENTER
    pit_count = o2.PitLaneCount.YES
if args.pit_leave:
    pit_trigger = o2.PitLaneTrigger.LEAVE
    pit_count = o2.PitLaneCount.YES

# configure the system
system = o2.set_start_config(
        max_speed = CAR_LIMIT_MAX_SPEED,
        pit_lane_trigger = pit_trigger,
        pit_lane_count = pit_count,
        power_mean_value = o2.PowerMeanValue.PWM
)

# use internal timer for simplicity
timer = o2.RaceTimer()
timer.start()


SMARTRACE_SERVER = (args.smartrace, args.port)
SMARTRACE_SOCKET = None

def init_smartrace():
    global SMARTRACE_SOCKET

    server_address = f"ws://{SMARTRACE_SERVER[0]}:{SMARTRACE_SERVER[1]}"

    try:
        SMARTRACE_SOCKET = connect(server_address)

        SMARTRACE_SOCKET.send('{"type":"api_version"}')
        for _ in range(3):
            SMARTRACE_SOCKET.recv()
            sleep(1/20)
        SMARTRACE_SOCKET.send('{"type": "controller_set", "data": {"controller_id": "Z"}}')
        sleep(1/20)
        print("Smartrace connected")
        return True
    except:
        print("Smartrace connection broken")
        SMARTRACE_SOCKET = None
        return False

def ws_message_create(lap_time):
    # see check_isr_data
    # lap_time[0] is either FL (finish line), PE (pit enter), PL (pit leave)
    # lap_time[1] is the card id: 1,2 or 3
    # lap_time[2] is the timestamp in ms / NOTE: oxigen provides timestamps in cs not ms!!!
    if lap_time[0] == 'FL':
        return '{"type":"analog_lap","data":{"timestamp":' + str(lap_time[2]*10) + ',"controller_id":' + str(
            lap_time[1]) + '}}'
    if lap_time[0] == 'PE':
        return '{"type":"analog_pit_enter","data":{"controller_id":' + str(lap_time[1]) + '}}'
    if lap_time[0] == 'PL':
        return '{"type":"analog_pit_leave","data":{"controller_id":' + str(lap_time[1]) + '}}'
    return ''

def send_smartrace_fl(car_id, time):
    if SMARTRACE_SOCKET is not None:
        msg = ws_message_create(('FL', car_id, time))
        SMARTRACE_SOCKET.send(msg)

def send_smartrace_pit(car_id, time, pit_enter = True):
    if SMARTRACE_SOCKET is not None:
        if pit_enter:
            msg = ws_message_create(('PE', car_id, time))
            SMARTRACE_SOCKET.send(msg)
        else:
            msg = ws_message_create(('PL', car_id, time))
            SMARTRACE_SOCKET.send(msg)


# catch the events
@o2.events.new_lap_event.connect
def lap(car_id, lap_count, timestamp, laptime, info_flag):
    print(f"ID{car_id}: new lap ({lap_count}) at {timestamp}cs")
    send_smartrace_fl(car_id, timestamp)

@o2.events.pit_lane_enter_event.connect
def pit_enter(car_id, timestamp):
    print(f"ID{car_id}: pit enter at {timestamp}cs")
    send_smartrace_pit(car_id, timestamp, pit_enter=True)

@o2.events.pit_lane_leave_event.connect
def pit_leave(car_id, timestamp):
    print(f"ID{car_id}: pit leave at {timestamp}cs")
    send_smartrace_pit(car_id, timestamp, pit_enter=False)

@o2.events.all_cars_on_track_event.connect
def all_cars_on_track(value, car_list):
    if value is False:
        print("EMERGENCY! SAFETY CAR OUT!")
        o2.set_system_max_speed(CAR_LIMIT_SAFETY_CAR_SPEED, system, timer)

        for car_id in car_list:
            print(f"Car ID{car_id} had an accident!")
    else:
        o2.set_system_max_speed(CAR_LIMIT_MAX_SPEED, system, timer)


# init the dongle
print(f"Connecting to the dongle at {args.dongle}...")
o2.dongle.connect(args.dongle)

#start the race
o2.set_race_state(
    new_state=o2.RaceState.RUNNING,
    sys=system,
    timer=timer
)

if args.pit_speed:
    o2.set_pit_stop_speed_limit(pit_speed=args.pit_speed, car_id=0, sys=system, timer=timer)

print("Oxigen configuration completed")

print("Starting Smartrace websocket client...")
if init_smartrace():
    while CONTINUE_LOOP:
        try:
            o2.dongle.check_data_waiting()
            # TODO: break loop if connection lost
            # use websockets.exceptions.ConnectionClosed
        except KeyboardInterrupt:
            CONTINUE_LOOP = False
            SMARTRACE_SOCKET.close()

print('Exiting :(')