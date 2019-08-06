#!/usr/bin/env python3

import os
from pathlib import Path
from random import SystemRandom
import subprocess
import sys
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pygame

VOLUME_LEVEL_PERCENT = .42
SNOOZE_TIME = 5 * 60


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
    """ Set the system volume. This will unfortunately be different on different systems. """
    subprocess.run(["amixer", "set", "Master", "--", str(percent * 100) + "%"])


def get_sound():
    random = SystemRandom()
    sound = random.choice(os.listdir('.'))
    while os.path.isdir(sound):
        os.chdir(sound)
        sound = random.choice(os.listdir('.'))
    return sound 


def play_sound():
    pygame.init()
    sound = get_sound()
    print("Playing " + sound)
    try:
        try:
            pygame.mixer.music.load(sound)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("Playing " + sound + " failed. Trying again.")
            play_sound()
    except RecursionError:
        print(f"Failed to find playable file. The directory for alarms is {get_alarms_location()}.")
        sys.exit(2)


def snooze(seconds):
    pygame.mixer.music.pause()
    time.sleep(seconds)
    main()


def show_dialog() -> bool:
    dialog = Gtk.MessageDialog(secondary_text="Good morning, I suppose.")
    dialog.set_title("Alarm")
    dialog.set_icon_name("audio-volume-high")
    dialog.add_button("Stop", 0)
    dialog.add_button("Snooze", 1)
    out = dialog.run()
    dialog.destroy()
    return bool(out)


def main():
    set_volume(VOLUME_LEVEL_PERCENT)
    os.chdir(str(get_alarms_location()))
    play_sound()
    out = show_dialog()
    if out:
        print("Snoozing")
        snooze(SNOOZE_TIME)
    pygame.mixer.music.pause()


if __name__ == "__main__":
    main()
