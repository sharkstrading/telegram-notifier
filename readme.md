# Telegram notifier

Telegram notifier that can be used as an alarm clock. Use this app to be awakened at a set time, but only if there are new messages.

This app was made to listen on one or more channels. These channels can be listened to using the `chatId`.

## Obtaining the chatId

For this you need to create a bot with the BotFather bot, and the bot needs to be activated/whitelisted in order to be able to receive messages from it.

A chat needs to be set up, and the ID of the chat is the explicit whitelisting of communications between the bot and you/your channel.
 
How to obtain the `chatId`:
- send a message to the bot/channel in which the bot resides
- then, go to `https://api.telegram.org/bot<YourBOTToken>/getUpdates` and find the "id" field of the "chat" object
- add this `chatId` to the list of chatIds in the config file
- the `chatIds` must be added as Integers

## Target system

This app was created to run on a Raspberry PI with speakers/headphones connected to it.

## Obtaining media files

Media files can be obtained from websites like https://quicksounds.com/

## Running the application on a Raspberry PI

```
cp config.example/config.yml config/config.yml
# fill in the values in config.yml
# then, set up the Python virtual environment with the correct dependencies
bash ./raspi-1-setup.sh
# then, start the app
bash ./raspi-1-run.sh
```

Note: `bash` is needed for the `source` command, `sh` won't work in this case