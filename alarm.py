#!/usr/bin/env python3.5

from pathlib import Path
import os
import random
import subprocess
import sys

from gpiozero import Button
import pygame

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

def main():
    set_volume(95)
    os.chdir(str(get_alarms_location()))
    sounds = os.listdir()
    sound = random.choice(sounds)
    pygame.init()
    pygame.mixer.music.load(sound)
    button = Button(21)
    pygame.mixer.music.play(-1)
    #ps = subprocess.run(['zenity', '--question'], stdout=subprocess.PIPE)
    #resp = ps.stdout.decode('ascii').strip()
    button.wait_for_press()
    pygame.mixer.music.pause()

if __name__ == '__main__':
    main()
