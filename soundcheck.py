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

with open(config_file, 'r') as file:
    config = yaml.safe_load(file)

if config['soundFile'] is None:
    logger.error("Missing sound file reference, cannot continue!")

    sys.exit(1)

sound = Sound()
sound.play_mp3(config['soundFile'])