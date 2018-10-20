#!/usr/bin/env python3.7
import argparse
import os
from pathlib import Path
import subprocess
import sys

from addalarm import get_crontab

def get_num(kind):
    r = ''
    while not r.isnumeric():
        r = input(kind + ': ')
    return r

def main():
    parser = argparse.ArgumentParser(description='Delete a scheduled alarm.')
    parser.add_argument('-a', '--all', action='store_true', help='Delete all alarms.')
    args = parser.parse_args()
    start = '# Alarms'
    file_path = Path('.tmpcron')
    crontab = get_crontab().split('\n')
    alarms = None
    for i, line in enumerate(crontab):
        if line == start:
            r = range(i + 1, len(crontab))
            alarms = [crontab[j] for j in r]
            for j in r:
                crontab.pop(len(crontab) - 1)
    if alarms is None or len([a for a in alarms if a.strip() != '']) == 0:
        print('There are no alarms!')
        return
    if not args.all:
        for i, line in enumerate(alarms):
            if line.strip() != '':
                print(str(i) + ':', line)
        try:
            n = int(get_num('Alarm to delete'))
        except KeyboardInterrupt:
            sys.exit()
        alarms.pop(n)
        crontab += alarms
        final = '\n'.join(crontab)
    else:
        final = '\n'.join(crontab) + '\n' 
    with file_path.open('w') as f:
        f.write(final)
    subprocess.run(['crontab', str(file_path)])
    os.remove(str(file_path))

if __name__ == '__main__':
    main()
