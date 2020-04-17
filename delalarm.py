#!/usr/bin/env python3

import argparse
import json
import os

TIMES_LOCATION = os.path.expanduser("~/.alarm-times.json")


def get_times(path):
    with open(TIMES_LOCATION) as file:
        return json.load(file)


def write_times(times, path):
    with open(TIMES_LOCATION, "w") as file:
        json.dump(times, file)


def ask_for_choice(times):
    for i, v in enumerate(times):
        print(f"{i}: {v}")
    valid = False
    choice = None
    while not valid:
        choice = input("Which should be deleted (-1 for none)? ").strip()
        if choice.isdigit() and int(choice) in range(len(times)):
            valid = True
        elif int(choice) == -1:
            return None
        else:
            print("Invalid choice.")
    return int(choice)


def main():
    parser = argparse.ArgumentParser(description='Delete a scheduled alarm.')
    parser.add_argument('-a', '--all', action='store_true', help='Delete all alarms.')
    args = parser.parse_args()
    times = get_times(TIMES_LOCATION)
    if len(times) == 0:
        print("There are no alarms to remove.")
        return
    if args.all:
        times = []
    else:
        choice = ask_for_choice(times)
        if choice is not None:
            del times[choice]
    write_times(times, TIMES_LOCATION)


if __name__ == '__main__':
    main()
