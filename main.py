#!/usr/bin/env python3

import sys
import yaml
from crontabs import Cron, Tab

from telegram_notifier import TelegramNotifier
from sound import Sound

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
logger.info(
    f"The application will be run every {cron_run_every_seconds} seconds between {cron_business_hours_start} and {cron_business_hours_end} hours according to system time")
logger.info("")

telegram_notifier = TelegramNotifier(config)

Cron().schedule(
    Tab(
        name='telegram-notifier'
    ).run(
        telegram_notifier.period
    ).every(
        seconds=cron_run_every_seconds
    ).during(
        business_hours
    )
).go()
