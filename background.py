#!/usr/bin/python3

import json
import os
import subprocess
import threading
import time

import alarm

TIMES_LOCATION = os.path.expanduser("~/.alarm-times.json")


def get_times(path):
    with open(TIMES_LOCATION) as file:
        return json.load(file)


def is_alarm_time(ct, times):
    for t in times:
        day_matches = False
        if "day_range" in t.keys():
            endpts = [int(n) for n in t["day_range"].split("-")]
            if ct.tm_wday in range(endpts[0], endpts[1] + 1):
                day_matches = True
        if "day" in t.keys():
            if ct.tm_wday == t["day"]:
                day_matches = True
        if day_matches and ct.tm_hour == t["hour"] and ct.tm_min == t["minute"]:
            return True
    return False


def execute_alarm():
    alarm_thread = threading.Thread(target=lambda: subprocess.run(["./alarm.py"]))
    #alarm_thread = threading.Thread(target=alarm.run)
    alarm_thread.start()


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    while True:
        try:
            current_time = time.localtime()
            times = get_times(TIMES_LOCATION)
            if is_alarm_time(current_time, times):
                print("Alarm triggering...")
                execute_alarm()
            if current_time.tm_sec == 0:
                time.sleep(60)
            else:
                time.sleep(60 - current_time.tm_sec)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
