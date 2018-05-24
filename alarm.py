#!/usr/bin/env python3.5

from pathlib import Path
import os
import random
#import subprocess
import sys

from gpiozero import Button
import pygame

def get_alarms_location():
    config_path = Path('~/.alarms-location').expanduser()
    default = Path('~/alarms').expanduser()
    try:
        with config_path.open() as f:
            return f.read().strip('\n')
    except FileNotFoundError:
        with config_path.open('w') as f:
            f.write(default)
        return default

def main():
    os.chdir(get_alarms_location())
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
    return
