"""
Telegram to RSS web server

Run server: uvicorn main:app --reload --host 0.0.0.0 --port 8091

For detailed setup, deployment and run instructions see readme.md file

© 2021 MediaMonitoringBot, written by Maksym Trineiev
"""

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

import logging
logging.basicConfig(
    filename=config['Logging']['FILE_NAME'],
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=int(config['Logging']['LEVEL']))

from feedgen.feed import FeedGenerator
from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from markdown2 import markdown
from telethon import TelegramClient, sync
from telethon.tl.types import PeerChannel
from telethon.tl.functions.channels import GetFullChannelRequest


api_id = config['Telegram']['API_ID']
api_hash = config['Telegram']['API_HASH']

client = TelegramClient('tg2rss', api_id, api_hash)

templates = Jinja2Templates(directory='templates')
app = FastAPI()

@app.get('/', response_class=HTMLResponse)
async def home_page(request: Request):
    """
    Displays home page form templates/index.html
    """
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/channel/{channel_alias}')
async def create_rss(channel_alias: str, request: Request):
    """
    Get posts from the channel and return rss-feed
    """
    try:
        await client.start()
        entity = await client.get_entity(channel_alias)
        channel = await client.get_entity(PeerChannel(entity.id))
    except Exception as e:
        warn = f"{str(e)}, request: '{channel_alias}'"
        logging.warning(warn)
        return warn

    ch_full = await client(GetFullChannelRequest(channel=channel))
    logging.info(f"'{channel.username}' requested")

    fg = FeedGenerator()
    fg.title(f'{channel.title} (@{channel.username}, id:{channel.id})')
    fg.subtitle(ch_full.full_chat.about)
    fg.link(href=f'https://t.me/s/{channel.username}', rel='alternate')
    fg.generator(config['RSS']['GENERATOR'])
    fg.language(config['RSS']['LANGUAGE'])

    async for message in client.iter_messages(channel,
                            limit=int(config['RSS']['RECORDS'])):
        if not (config['RSS'].getboolean('SKIP_EMPTY') and not message.text):
            fe = fg.add_entry(order='append')
            fe.guid(guid=f'https://t.me/{channel.username}/{message.id}',
                permalink=True)
            fe.content(markdown(message.text))
            fe.published(message.date)

    return Response(content=fg.rss_str(), media_type='application/xml')


if __name__ == '__main__':
    print(__doc__)
