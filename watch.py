#!/usr/bin/python3
import sys
import select
import time
import datetime as dt
import signal

def start(start_offset: int = 0):
    start_time = time.time()
    paused = False
    paused_time = None

    # Signal handler for Ctrl+C
    def signal_handler(sig, frame):
        nonlocal paused, paused_time, start_time
        if paused:
            # If already paused, a second Ctrl+C exits the program.
            print("\nCtrl+C pressed while paused. Exiting...")
            sys.exit(0)
        else:
            paused = True
            paused_time = time.time()
            print("\nPaused (via Ctrl+C)! Press ENTER or Ctrl+C to resume...")

    # Register our custom signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    print("Press ENTER to toggle pause/resume the timer.")
    while True:
        try:
            # Non-blocking check for input on stdin
            dr, _, _ = select.select([sys.stdin], [], [], 0)
        except InterruptedError:
            # If select is interrupted by a signal, just continue.
            continue

        if dr:
            # Read the input line.
            line = sys.stdin.readline()
            # If the line is empty (just Enter pressed), toggle pause/resume.
            if line.strip() == '':
                if not paused:
                    paused = True
                    paused_time = time.time()
                    print("\nPaused! Press ENTER or Ctrl+C to resume...")
                else:
                    paused = False
                    # Adjust start_time so that the paused period isn't counted.
                    start_time += time.time() - paused_time
                    paused_time = None

        if not paused:
            current_sec = (time.time() - start_time) + start_offset
            # Clear the previous line and print the current elapsed time.
            print(" " * 40, end="\r", flush=True)
            print(f"{dt.timedelta(seconds=current_sec)}, seconds: {int(current_sec)}", end="\r", flush=True)
        time.sleep(0.1)

if __name__ == '__main__':
    print("How many seconds to offset by?")
    offset = input()
    offset = int(offset) if offset.strip() != "" else 0
    start(offset)
