#!/usr/local/bin/python3

import time
import datetime as dt
import signal


paused = False
paused_time = None
start_time = time.time()


def signal_handler(sig, frame):
    global paused, paused_time, start_time
    # if second ctrl c
    if paused:
        exit(0)
    else:
        paused_time = time.time()
    paused = not paused


signal.signal(signal.SIGINT, signal_handler)


def start(start_offset=0):
    global paused, start_time, paused_time
    print()
    while True:
        if not paused:
            current_sec = (time.time() - start_time) + start_offset
            print(" " * 40, end="\r", flush=True)
            print(f"{dt.timedelta(seconds=current_sec)}, seconds: {int(current_sec)}", end="\r", flush=True)
            time.sleep(0.1)
        else:
            print()
            print("PAUSED! press enter to resume...")
            input()
            paused = False
            start_time += time.time() - paused_time
            paused_time = None


if __name__ == '__main__':
    start()
