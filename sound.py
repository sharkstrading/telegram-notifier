#!/usr/bin/env python3

from pydub import AudioSegment
from pydub.playback import play


class Sound:
    def play_mp3(self, filename):
        song = AudioSegment.from_mp3(filename)
        play(song)
