# Telegram channel RSS feed generation

## Description
Python script using Telegram-client API for generation RSS feed from Telegram channels

## Setup and deployment
- `git clone https://github.com/mtrineyev/tgtorss.git`
- `cd tgtorss`
- `cp config.ini.example config.ini`
- `nano config.ini` and set variables
- `sudo apt-get install python3-dev`
- `sudo apt-get install python3-venv`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

## To run server

- `cd ~/tgtorss`
- `nano tgtorss.sh`
```
#!/bin/bash
cd ~/tgtorss
source env/bin/activate
uvicorn main:app --reload --host your.server.internal.ip --port 8091
```
- `chmod +x tgtorss.sh`
- `./tgtorss.sh`

Note: on the first request to the server you will be asked for Telegram phone and password used for the `API_ID`

## To test server
Open in any browser `localhost:8091`
  
## Licence
The script is free software written by Maksym Trineyev (mtrineyev@gmail.com).

It comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.
