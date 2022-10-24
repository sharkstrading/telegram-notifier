#!/usr/bin/env python3

from pydub import AudioSegment
from pydub.playback import play
import yaml

from sound import Sound

# -------------------------------------------------------------------
# vars
# -------------------------------------------------------------------

config_file = "config/config.yml"
config = None

# -------------------------------------------------------------------
# sanity checks
# -------------------------------------------------------------------

print("-------------------------------------------------------------------")
print("Soundcheck")
print("-------------------------------------------------------------------")
print("")

with open(config_file, 'r') as file:
    config = yaml.safe_load(file)

if config['soundFile'] is None:
    print(" ❌ Missing sound file reference, cannot continue!")

    sys.exit(1)

print(" ✅ Configuration OK")
print("Playing sound ...")

sound = Sound()
sound.play_mp3(config['soundFile'])

print(" ✅ Done playing sound. Did you hear it?")