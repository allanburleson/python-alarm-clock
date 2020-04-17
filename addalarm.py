#!/usr/bin/env python3
import argparse
import json
import os
import sys

TIMES_LOCATION = os.path.expanduser("~/.alarm-times.json")


def fix_args(args):
    if not args["minute"]:
        args["minute"] = 0
    for k, v in args.copy().items():
        if v is None:
            del args[k]


def check_args(args):
    assert (args["day"] is not None) or args["day_range"] is not None, \
        "At least one of day and day range must be given"
    assert args["hour"] is not None, "Hour must be given"
    if args["day_range"] is not None:
        assert len(args["day_range"]) == 3 and ''.join(args["day_range"].split("-")).isdigit() \
               and args["day_range"][1] == "-", "Range is formatted incorrectly"


def write(args, file_path):
    print(args)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([args], f)
    else:
        with open(file_path, "r+") as f:
            j = json.load(f)
            # Overwrite beginning of file
            f.seek(0)
            j.append(args)
            json.dump(j, f)
            # Erase old leftover data
            f.truncate()


def main():
    parser = argparse.ArgumentParser(
        description='Add an alarm.')
    parser.add_argument('-m', '--minute', type=int, help='If left blank defaults to 0.')
    parser.add_argument('-r', '--hour', type=int, help='Uses 24-hour time.')
    parser.add_argument('-d', '--day', type=int,
                        help='Weekday as a number. Monday is 0.')
    parser.add_argument('-g', '--day-range', type=str,
                        help='Enter start and end days, separated by a hyphen.')
    args = vars(parser.parse_args())
    if set(args.values()) == {None}:
        parser.parse_args(['-h'])
        sys.exit()
    check_args(args)
    fix_args(args)
    write(args, TIMES_LOCATION)


if __name__ == '__main__':
    main()
