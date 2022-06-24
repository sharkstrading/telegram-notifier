#!/usr/bin/env python3

import sys
import time

import telegram
import yaml
import itertools
from crontabs import Cron, Tab
from pydub import AudioSegment
from pydub.playback import play

logger = Cron.get_logger()

# -------------------------------------------------------------------
# vars
# -------------------------------------------------------------------

config_file = "config/config.yml"
config = None
latest_update = None
# only inquire after these types of updates
allowed_updates = "channel_post"

# -------------------------------------------------------------------
# functions
# -------------------------------------------------------------------

def period(config):
    # Grab an instance of the crontab logger and write to it.
    bot = telegram.Bot(token=str(config['telegram']['token']))

    if latest_update:
        logger.info(f"Getting updates since updateID {latest_update.update_id} ...")
        updates = bot.get_updates(allowed_updates=allowed_updates, offset=latest_update.update_id)
    else:
        logger.info(f"Getting updates ...")
        updates = bot.get_updates(allowed_updates=allowed_updates)

    if updates:
        logger.info(f"Updates found, processing ...")
        handle_updates(updates, config)
    else:
        logger.info(" ✅ Everything is up-to-date")

def handle_updates(updates, config):
    for update in updates:
        if hasattr(update, 'effective_chat') and hasattr(update.effective_chat, 'id') and int(update.effective_chat.id) in config['telegram']['chatIDs']:
            handle_update(update, config)
        else:
            logger.info(f"Received invalid message, ignoring")

def handle_update(update, config):
    logger.info(f"Update found for chatID {update.effective_chat.id}. Sounding alarm ...")
    set_latest_update(update)

    for _ in itertools.repeat(None, int(config['repeatAlarm'])):
        play_mp3(config['soundFile'])

        time.sleep(config['sleepBetweenAlarms'])
        
def set_latest_update(update):
    if latest_update is None or update.update_id > latest_update.update_id:
        latest_update = update
        logger.info(f"The latest updateID changed to {latest_update.update_id} just now")

def play_mp3(filename):
    song = AudioSegment.from_mp3(filename)
    play(song)

def business_hours(timestamp):
    return cron_business_hours_start <= timestamp.hour < cron_business_hours_end

# -------------------------------------------------------------------
# sanity checks
# -------------------------------------------------------------------

with open(config_file, 'r') as file:
    config = yaml.safe_load(file)

if config['telegram'] is None:
    logger.error("Missing Telegram settings, cannot continue!")

    sys.exit(1)

if config['telegram']['chatIDs'] is None:
    logger.error("Missing Telegram chat IDs, cannot continue!")

    sys.exit(1)

if config['soundFile'] is None:
    logger.error("Missing sound file reference, cannot continue!")

    sys.exit(1)

cron_business_hours_start = int(config['cronBusinessHoursStart'])
cron_business_hours_end = int(config['cronBusinessHoursEnd'])
cron_run_every_seconds = int(config['cronRunEverySeconds'])

logger.info("---------------------------------------------------------------------")
logger.info("telegram-notifier starting up ...")
logger.info("---------------------------------------------------------------------")

logger.info("")
logger.info(f"The application will be run every {cron_run_every_seconds} seconds between {cron_business_hours_start} and {cron_business_hours_end} hours according to system time")
logger.info("")

# get the latest updates if any
bot = telegram.Bot(token=str(config['telegram']['token']))
updates = bot.get_updates(allowed_updates=allowed_updates)

if updates:
    # by adding an offset, previous messages will be ignored
    offset = 1
    latest_update = updates[-1]
    logger.info(f"Latest update at startup time: {latest_update.update_id}")
    latest_update.update_id = latest_update.update_id + offset
else:
    logger.info(f"Latest update: (none)")

Cron().schedule(
    Tab(
        name='telegram-notifier'
    ).run(
        period, config
    ).every(
        seconds=cron_run_every_seconds
    ).during(
        business_hours
    )
).go()