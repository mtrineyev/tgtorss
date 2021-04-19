# Telegram channel RSS feed generation


## Description
Python script using Telegram-client API for generation RSS feed from Telegram channels.

Examples:
- to get RSS feed from the public channel: http://localhost:8091/channel/name.
- to get RSS feed from the private channel: http://localhost:8091/channel/joinchatAAAAAAXXXXXXXXXX (without '/' in inviting link). The user should NOT be joined to the private channel. The private channel will be joined automatically.


## Setup and deployment
- `git clone https://github.com/mtrineyev/tgtorss.git`
- `cd tgtorss`
- `cp config.ini.example config.ini`
- `nano config.ini` and set the variables as described in the comments
- `sudo apt-get install python3-dev`
- `sudo apt-get install python3-venv`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python connect.py` and enter your phone and the code you will recieve
- `nano tgtorss.sh` and copy the code below
```
#!/bin/bash
cd ~/tgtorss
source venv/bin/activate
uvicorn main:app --reload --host your.server.internal.ip --port 8091
deactivate
```
- `chmod +x tgtorss.sh`


## To run the server
- `~/tgtorss/tgtorss.sh`

IMPORTANT:
1. Do not make more than 30 requests per seconds to a new channels, otherwise your ID may be banned to several hours. When a channel has been accessed first time its information hashed and next requests to the channel are safe. You can work with the hash file using the tool `hash.py`.
2. If you will delete `*.session` file you should also delete `hash.pickle` file and re-connect to the Telegram.


## To test the server
`curl http://your.server.internal.ip:8091/channel/bbcukrainian`


## The tools
- `connect.py` - creates new connection to Telegram client or shows information about active connection, if any
- `hash.py` - hash file viewing/keys deleting tool


## The licence
The script is free software written by Maksym Trineyev (mtrineyev@gmail.com).

It comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.
