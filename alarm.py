#!/usr/bin/env python3

import os
from pathlib import Path
from random import SystemRandom
import subprocess
import time

import pygame

VOLUME_LEVEL_PERCENT = .2


def get_alarms_location():
    """
    Returns the location of the alarms directory as
    defined in ~/.alarms-location. Default is ~/alarms.
    """
    config_path = Path("~/.alarms-location").expanduser()
    default = Path("~/alarms").expanduser()
    try:
        with config_path.open() as f:
            return f.read().strip("\n")
    except FileNotFoundError:
        with config_path.open("w") as f:
            f.write(str(default))
        return default


def set_volume(percent):
    """ Set the system volume. This may be different on different systems. """
    subprocess.run(["amixer", "set", "Master", "--", str(percent * 100) + "%"])


def get_sound():
    random = SystemRandom()
    sound = random.choice(os.listdir())
    while os.path.isdir(sound):
        os.chdir(sound)
        sound = random.choice(os.listdir())
    return sound 


def play_sound():
    pygame.init()
    sound = get_sound()
    print("Playing " + sound)
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
    except pygame.error:
        print("Playing " + sound + " failed. Trying again.")
        play_sound()


def snooze(seconds):
    pygame.mixer.music.pause()
    time.sleep(seconds)
    main()


def main():
    set_volume(VOLUME_LEVEL_PERCENT)
    os.chdir(str(get_alarms_location()))
    play_sound()
    while pygame.mixer.music.get_busy():
        pass
    return
    """# turn display on
    ps = subprocess.Popen(["echo", "on 0"], stdout=subprocess.PIPE)
    subprocess.run(["cec-client", "-s", "-d", "1"], stdin=ps.stdout)
    ps = subprocess.run(["zenity", "--question", "--title", "Alarm",
        "--ok-label", "Stop", "--cancel-label", "Snooze", "--text",
        "Good morning!"], stdout=subprocess.PIPE)
    resp = ps.returncode
    if int(resp):
        print("Snoozing")
        snooze(5 * 60)
    pygame.mixer.music.pause()
    # turn display off
    ps = subprocess.Popen(["echo", "standby 0"], stdout=subprocess.PIPE)
    subprocess.run(["cec-client", "-s", "-d", "1"], stdin=ps.stdout)"""


if __name__ == "__main__":
    main()
