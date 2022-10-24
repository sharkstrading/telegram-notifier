#!/usr/bin/env python3

import itertools
import time
import telegram
from crontabs import Cron

class TelegramNotifier:
    def __init__(self, config):
        self.config = config
        self.sound = Sound()
        self.allowed_updates = "channel_post"
        self.logger = Cron.get_logger()
        self.bot = telegram.Bot(token=str(config['telegram']['token']))
        self.latest_update_id = 0
        self.initialize_updates()

    # get the latest updates if any
    def initialize_updates(self):
        updates = self.bot.get_updates(allowed_updates=self.allowed_updates)

        if updates:
            # by adding an offset, previous messages will be ignored
            offset = 1
            self.latest_update_id = updates[-1].update_id
            self.logger.info(f"Latest update: {self.latest_update_id}")
            self.latest_update_id = self.latest_update_id + offset
        else:
            self.logger.info(f"Latest update: (none)")

    # run this method every period
    def period(self):
        if self.latest_update_id != 0:
            self.logger.info(f"Getting updates since updateID {self.latest_update_id} ...")
            updates = self.bot.get_updates(allowed_updates=self.allowed_updates, offset=self.latest_update_id)
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
        self.set_latest_update(update, 1)

        for _ in itertools.repeat(None, int(self.config['repeatAlarm'])):
            sound.play_mp3(filename)

            time.sleep(self.config['sleepBetweenAlarms'])

    def set_latest_update(self, update, offset):
        update_id = update.update_id
        if self.latest_update_id == 0 or update_id > self.latest_update_id:
            self.latest_update_id = update_id + offset
            self.logger.info(f"The latest updateID changed to {self.latest_update_id} just now")

    def __str__(self):
        return f"{TelegramNotifier}"
