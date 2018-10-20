#!/usr/bin/env python3.5

from pathlib import Path
from math import inf
import os
import random
import signal
import subprocess
import sys
import time

from gpiozero import Button
import pygame

x = 0

def get_alarms_location():
    '''
    Returns the location of the alarms directory as
    defined in ~/.alarms-location. Default is ~/alarms.
    '''
    config_path = Path('~/.alarms-location').expanduser()
    default = Path('~/alarms').expanduser()
    try:
        with config_path.open() as f:
            return f.read().strip('\n')
    except FileNotFoundError:
        with config_path.open('w') as f:
            f.write(str(default))
        return default

def set_volume(percent):
    ''' Set the system volume. This may be different on different systems. '''
    subprocess.run(['amixer', 'set', 'PCM', '--', str(percent) + '%'])

def play_sound():
    try:
        sounds = os.listdir()
        sound = random.choice(sounds)
        pygame.init()
        item = random.choice(os.listdir())
        while os.path.isdir(item):
            os.chdir(item)
            item = random.choice(os.listdir())
        pygame.init()
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play(-1)
    except:
        play_sound()



def main():
    global x
    set_volume(77)
    os.chdir(str(get_alarms_location()))
    play_sound()
    b = Button(21)
    t = inf
    def incrx():
        global x
        x += 1
    b.when_pressed = incrx
    while 1:
        if time.time() - t > 1:
            break
        if x >= 1 and t == inf:
            t = time.time()
            pygame.mixer.music.pause()

    if x > 8:
        print('held, snoozing')
        #pygame.mixer.music.pause()
        del b
        x = 0
        time.sleep(5 * 60)
        main()
    else:
        print('pressed, turning off')

if __name__ == '__main__':
    main()
