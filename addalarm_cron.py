#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import subprocess
import sys


def get_alarm_location():
    config_path = Path('~/.alarm-location').expanduser()
    default = Path('~/bin/alarm.py').expanduser()
    try:
        with config_path.open() as f:
            return f.read().strip('\n')
    except FileNotFoundError:
        with config_path.open('w') as f:
            f.write(str(default))
        return default


def create_alarms_for_range(args):
    days = args['day_range'].split('-')
    assert len(days) == 2, 'Must use range of two days'
    assert ''.join(days).digit(), 'Days must be numbers'
    days[0], days[1] = int(days[0]), int(days[1])
    for day in days:
        assert 0 <= day <= 7, 'Days must be at least 0 and no greater than 7'
    convert_args(args)
    lines = []
    for i in range(days[0], days[1] + 1):  # Make a line for each day in the day range
        args['day_of_week'] = str(i)
        lines.append(gen_line(args))
    return lines


def gen_line(args):
    # Make a copy of args without day_range
    a = args.copy()
    a.pop('day_range')
    return ' '.join(a.values()) + ' ' + 'DISPLAY=:0 ' + str(get_alarm_location())


def convert_args(args):
    for k, v in args.items():
        if v is None:
            args[k] = '*'
        else:
            args[k] = str(v)


def write(crontab, lines, file_path):
    file_path.write_text(crontab + '\n'.join(lines) + '\n')
    assert subprocess.run(['crontab', str(file_path)]).returncode == 0
    os.remove(str(file_path))


def get_crontab():
    crontab = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE).stdout
    return crontab.decode('ascii')


def main():
    parser = argparse.ArgumentParser(
            description='Add an alarm. Blank fields default to "*".')
    parser.add_argument('-m', '--minutes', type=int)
    parser.add_argument('-r', '--hours', type=int, help='Uses 24-hour time.')
    parser.add_argument('--day-of-month', type=int)
    parser.add_argument('-n', '--month', type=int)
    parser.add_argument('-d', '--day-of-week', type=int,
                        help='Weekday as a number. Sunday = 0.')
    parser.add_argument('-g', '--day-range', type=str,
                        help='Enter start and end days, separated by a hyphen.')
    start = '# Alarms\n'
    file_path = Path('~/.tmpcron').expanduser()
    crontab = get_crontab()
    if start not in crontab:
        crontab += start
    args = vars(parser.parse_args())
    if set(args.values()) == {None}:
        parser.parse_args(['-h'])
        sys.exit()
    if args['day_range'] is not None:
        lines = create_alarms_for_range(args)
        write(crontab, lines, file_path)
    else:
        convert_args(args)
        line = gen_line(args)    
        write(crontab, [line], file_path)


if __name__ == '__main__':
    main()
