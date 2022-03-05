# Tidal-DL-Bot-TG
Telegram bot to download Songs from Tidal.

## Features

- Download Tracks/Albums/Mix/Playlist from Tidal
- Quality available upto Master-FLAC
- Search songs inline using Tidal-API
- Store downloaded songs to Channel/Group
- Bot can configured for Public or Private use

**⚠️ Download Feature Won't Work Without A Tidal Premium Account ⚠️**

## Heroku Deploy
Use the below button to deploy the bot in Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Variables Details
**-> Required variables**

- `TG_BOT_TOKEN` - The Telegram Bot Token. (Get from [@BotFather](https://t.me/BotFather))
- `APP_ID` - Telegram account API ID. (Get it from [Telegram](https://my.telegram.org))
- `API_HASH` - Telegram account API HASH String. (Get it from [Telegram](https://my.telegram.org))
- `USER_SESSION` - Telegram account session string. (Generate from [HERE](https://replit.com/@vm703/Pyro-Session-Gen?lite=1&outputonly=1#main.py) or use any other Pyrogram Session Generator)
- `AUTH_CHAT` - List of Chat ID where Bot will work.
- `ADMINS` - List of User ID who has full access to the Bot.
- `ALLOW_DUMP` - Whether to store the downloaded files in any group/channel. (True/False)
- `SEARCH_CHANNEL` - ID of channel/gropup to search downloaded/other songs files direcly
- `IS_BOT_PUBLIC` - Whether to allow bot usage for public. (True/False)
- `TIDAL_REGION` - Country code for Tidal Song search. (In international format eg:IN)
- `TIDAL_SEARCH_LIMIT` - Limit the number of search results.
- `BOT_USERNAME` - Username of your bot.
- `OWNER_USERNAME` - Owner of the bot username (used for contact button, use any other username as you like)

**-> Optional variables**
- `LOG_CHANNEL_ID` - Group/Channel ID where bot stores all the downloaded files (Mandatory if set ALLOW_DUMP = True)
- `AUTH_USERS` - List of User ID who can use the bot (Only needed if IS_BOT_PUBLIC = False)
- `INLINE_THUMB` - Logo to be shown in inline search results. (Use CDN links for better performance)



## Bot Commads Details
#### Info about available commands for the bot
#### Copy paste these commands in BotFather
#### If you want to change the default commands go to [__init.py\_\_ Line 27](https://github.com/vinayak-7-0-3/Tidal-DL-Telegram/blob/90a176565bdf3002768c5be2840c7b81eb969cfb/bot/__init__.py#L27)

```
start - Start the bot
help - Shows Help Message
download - Download songs from Tidal
auth - Authorise a chat/user
auth_tidal - Sign in with Tidal Ac [ADMIN ONLY]
add_sudo - Add a user as Admin [ADMIN ONLY]
shell - Run shell cmds [ADMIN ONLY]
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

## Credits
#### Yarronzz - For his Tidal-dl CLI
