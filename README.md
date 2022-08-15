# Tidal-DL-Bot-TG
Telegram bot to download Songs from Tidal.

## Features

- Download Tracks/Albums/Mix/Playlist from Tidal
- Quality available upto Master-FLAC
- Search songs inline using Tidal-API
- Store downloaded songs to Channel/Group
- Bot can configured for Public or Private use
- Index Channel Feature for avoiding duplicate and search option
- Auto convert other music platform link to Tidal link 

**⚠️ Download Feature Won't Work Without A Tidal Premium Account ⚠️**

## Heroku Deploy
Use the below button to deploy the bot in Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Koyeb Deploy
Use the below button to deploy the bot in Koyeb.

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/vinayak-7-0-3/Tidal-DL-Telegram&branch=main&name=tidal-dl-tg&run_command=python%20-m%20bot&env[TG_BOT_TOKEN]=&env[APP_ID]=&env[API_HASH]=&env[USER_SESSION]=&env[AUTH_CHAT]=&env[ADMINS]=&env[ALLOW_DUMP]=False&env[IS_BOT_PUBLIC]=True&env[TIDAL_REGION]=IN&env[TIDAL_SEARCH_LIMIT]=10&env[BOT_USERNAME]=&env[OWNER_USERNAME]=&env[DATABASE_URL]=&env[ENV]=True)

- Fill all the Variables (In Environment Variable Section)
- For Database URL use Heroku Postgres or ElephantSQL

## Deploy Locally
Rename example.env to .env and fill all those required variables.
```
virtualenv -p python3 VENV
. ./VENV/bin/activate
pip install -r requirements.txt
python -m bot
```
- For Database URL use Heroku Postgres (if on Heroku) or ElephantSQL

## Variables Details
**-> Required variables**

- `TG_BOT_TOKEN` - The Telegram Bot Token. (Get from [@BotFather](https://t.me/BotFather))
- `APP_ID` - Telegram account API ID. (Get it from [Telegram](https://my.telegram.org))
- `API_HASH` - Telegram account API HASH String. (Get it from [Telegram](https://my.telegram.org))
- `AUTH_CHAT` - List of Chat ID where Bot will work. (Seperated by space)
- `ADMINS` - List of User ID who has full access to the Bot. (Seperated by space)
- `ALLOW_DUMP` - Whether to store the downloaded files in any group/channel. (True/False)
- `IS_BOT_PUBLIC` - Whether to allow bot usage for public. (True/False)
- `TIDAL_REGION` - Country code for Tidal Song search. (In international format eg:IN)
- `TIDAL_SEARCH_LIMIT` - Limit the number of search results.
- `BOT_USERNAME` - Username of your bot.
- `DATABASE_URL` - Postgres Database URL

**-> Optional variables**
- `LOG_CHANNEL_ID` - Group/Channel ID where bot stores all the downloaded files (Mandatory if set ALLOW_DUMP = True)
- `AUTH_USERS` - List of User ID who can use the bot (Seperated by space) (Only needed if IS_BOT_PUBLIC = False)
- `INLINE_THUMB` - Logo to be shown in inline search results. (Use CDN links for better performance)
- `ENV` - Set to True if using ENV Variables.
- `SEARCH_CHANNEL` - ID of channel/gropup to search downloaded/other songs files direcly
- `USER_SESSION` - Telegram account session string. (Required for Searching and Indexing to work) (Generate from [HERE](https://replit.com/@vm703/Pyro-Session-Gen?lite=1&outputonly=1#main.py) or use any other Pyrogram Session Generator)
- `MUSIC_CHANNEL_LINK` - For providing direct join link to the Music Storage Channel while searching for songs inline.
- `ALLOW_OTHER_LINKS` - If to allow automatic conversion of other music platform links to Tidal links while downloading. (Current API has a limit of 10 conversion per minute) (True/False)



## Bot Commads Details
#### Info about available commands for the bot
#### Tidal Authentication is done in the settings panel. Use /settings command
#### Copy paste these commands in BotFather
#### If you want to change the default commands go to [__init.py\_\_ Line 27](https://github.com/vinayak-7-0-3/Tidal-DL-Telegram/blob/90a176565bdf3002768c5be2840c7b81eb969cfb/bot/__init__.py#L27)

```
start - Start the bot
help - Shows Help Message
download - Download songs from Tidal
auth - Authorise a chat/user
settings - Open Settings Panel [ADMIN ONLY]
add_sudo - Add a user as Admin [ADMIN ONLY]
shell - Run shell cmds [ADMIN ONLY]
index - Index Search channel with Songs [ADMIN ONLY]
authed - Shows list of chats where bot is allowed to run
```

## Tidal Config Details
#### Tidal Download Settings can be configured by editing values in [.tidal-dl.json](https://github.com/vinayak-7-0-3/Tidal-DL-Telegram/blob/main/.tidal-dl.json)
#### The values can be as follows :-
- `addLyrics` - Whether to add lyrics to the song

- `apiKeyIndex` - Index number of the API 
**Available API Indexes are:-**\
0 - Fire TV (Formats:- Normal/High/HiFi)\
1 - Fire TV (Formats:- Master Only. For songs without master quality will give error)\
2 - Android TV (Formats:- Normal/High/Hifi)\
3 - TV (Formats:- Normal/High/HiFi/Master)\
4 - Android Auto (Formats:- Normal/High/HiFi/Master)

- `audioQuality` - Can be set to any of these :- Normal/High/Hifi/Master

- `downloadPath` - Where songs will be downloaded (set this to same as in the bot variable)

#### It is recommened not to change other values in the JSON

## JOIN [SUPPORT GROUP](https://t.me/weebzgroup) FOR HELP

## Credits
#### Yarronzz - For his [Tidal-dl CLI](https://github.com/yaronzz/Tidal-Media-Downloader)
#### Odesli/Songlink - For [API](https://www.notion.so/API-d0ebe08a5e304a55928405eb682f6741)