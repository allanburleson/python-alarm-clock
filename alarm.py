#!/usr/bin/python3

import os
from pathlib import Path
from random import SystemRandom
import subprocess
import sys
import time
from urllib.request import pathname2url

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gst', '1.0')
from gi.repository import Gst

VOLUME_LEVEL_PERCENT = .6
SNOOZE_TIME = 5 * 60

Gst.init()
playbin = Gst.ElementFactory.make("playbin", "playbin")


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
    subprocess.run(["pactl", "set-sink-mute", "0", "0"])
    subprocess.run(["pactl", "set-sink-volume", "0", str(int(percent * 100)) + "%"])


def get_sound():
    random = SystemRandom()
    files = os.listdir('.')
    sound = random.choice(files)
    while os.path.isdir(sound):
        os.chdir(sound)
        files = os.listdir('.')
        sound = random.choice(files)
    return sound 


def play_sound():
    sound = get_sound()
    print("Playing " + sound)
    try:
        playbin.props.uri = "file://" + pathname2url(os.path.abspath(sound))
        result = playbin.set_state(Gst.State.PLAYING)
        if result != Gst.StateChangeReturn.ASYNC:
            print(f"Error: {result}. Trying again.")
            play_sound()
    except RecursionError:
        print(f"Failed to find playable file. The directory for alarms is {get_alarms_location()}.")
        return 2


def snooze(seconds):
    playbin.set_state(Gst.State.NULL)
    time.sleep(seconds)
    run()


def show_dialog() -> bool:
    dialog = Gtk.MessageDialog(secondary_text="Good morning.")
    dialog.set_title("Alarm")
    dialog.set_icon_name("audio-volume-high")
    dialog.add_button("Stop", 0)
    dialog.add_button("Snooze", 1)
    out = dialog.run()
    dialog.destroy()
    #Gtk.main_quit()
    playbin.set_state(Gst.State.NULL)
    return bool(out)


def run():
    set_volume(VOLUME_LEVEL_PERCENT)
    os.chdir(str(get_alarms_location()))
    out = play_sound()
    if out is not None:
        return out
    out = show_dialog()
    if out:
        print("Snoozing")
        snooze(SNOOZE_TIME)


def main():
    out = run()
    sys.exit(out)


if __name__ == "__main__":
    main()
