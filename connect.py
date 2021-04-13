"""
Telegram client connection tool

For detailed setup, deployment and run instructions see readme.md file

Written by Maksym Trineiev
"""

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

from telethon import TelegramClient, sync

if __name__ == '__main__':
    try:
        client = TelegramClient(
            config['Telegram']['SESSION'],
            config['Telegram']['API_ID'],
            config['Telegram']['API_HASH'])
        client.start()
        user = client.get_me()
    except Exception as e:
        print(f"Can't connect to Telegram client. Reason: {str(e)}")
    else:
        print("Client connected as "\
            f"{user.first_name} {user.last_name} "\
            f"(Username: {user.username}, "\
            f"phone: +{user.phone})\n"\
            f"Session: {config['Telegram']['SESSION']}")
