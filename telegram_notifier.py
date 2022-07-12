#!/usr/bin/env python3

import itertools
import time
import telegram
from crontabs import Cron
from pydub import AudioSegment
from pydub.playback import play


class TelegramNotifier:
    def __init__(self, config):
        self.config = config
        self.allowed_updates = "channel_post"
        self.logger = Cron.get_logger()
        self.bot = telegram.Bot(token=str(config['telegram']['token']))
        self.latest_update = None
        self.initialize_updates()

    # get the latest updates if any
    def initialize_updates(self):
        updates = self.bot.get_updates(allowed_updates=self.allowed_updates)

        if updates:
            # by adding an offset, previous messages will be ignored
            offset = 1
            self.latest_update = updates[-1]
            self.logger.info(f"Latest update: {self.latest_update.update_id}")
            self.latest_update.update_id = self.latest_update.update_id + offset
        else:
            self.logger.info(f"Latest update: (none)")

    # run this method every period
    def period(self):
        if self.latest_update:
            self.logger.info(f"Getting updates since updateID {self.latest_update.update_id} ...")
            updates = self.bot.get_updates(allowed_updates=self.allowed_updates, offset=self.latest_update.update_id)
        else:
            self.logger.info(f"Getting updates ...")
            updates = self.bot.get_updates(allowed_updates=self.allowed_updates)

        if updates:
            self.logger.info(f"Updates found, processing ...")
            self.handle_updates(updates)
        else:
            self.logger.info(" ✅ Everything is up-to-date")

    def handle_updates(self, updates):
        for update in updates:
            if hasattr(update, 'effective_chat') and hasattr(update.effective_chat, 'id') and int(
                    update.effective_chat.id) in self.config['telegram']['chatIDs']:
                self.handle_update(update)
            else:
                self.logger.info(f"Received invalid message, ignoring")

    def handle_update(self, update):
        self.logger.info(f"Update found for chatID {update.effective_chat.id}. Sounding alarm ...")
        # add +1 to the update number so the app won't be triggered again
        # until a new message arrives
        self.set_latest_update(update+1)

        for _ in itertools.repeat(None, int(self.config['repeatAlarm'])):
            self.play_mp3(self.config['soundFile'])

            time.sleep(self.config['sleepBetweenAlarms'])

    def set_latest_update(self, update):
        if self.latest_update is None or update.update_id > self.latest_update.update_id:
            self.latest_update = update
            self.logger.info(f"The latest updateID changed to {self.latest_update.update_id} just now")

    def play_mp3(self, filename):
        song = AudioSegment.from_mp3(filename)
        play(song)

    def __str__(self):
        return f"{TelegramNotifier}"
