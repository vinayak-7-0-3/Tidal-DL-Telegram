import time
import aigpy
from bot import LOGGER
from bot.helpers.translations import lang
from bot.helpers.database.postgres_impl import TidalSettings
from bot.helpers.buttons.settings_buttons import tidal_auth_set
from bot.helpers.utils.media_search import check_duplicate

import bot.helpers.tidal_func.apikey as apiKey

from bot.helpers.tidal_func.tidal import *
from bot.helpers.tidal_func.enums import *
from bot.helpers.tidal_func.download import *
from bot.helpers.tidal_func.settings import TokenSettings, TOKEN

set_db = TidalSettings()

def __displayTime__(seconds, granularity=2):
    if seconds <= 0:
        return "unknown"

    result = []
    intervals = (
        ('weeks', 604800),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1),
    )

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

async def loginByWeb(bot, msg, c_id):
    try:
        url = TIDAL_API.getDeviceCode()
        await bot.edit_message_text(
            chat_id=c_id,
            message_id=msg.message.id, 
            text=lang.select.AUTH_NEXT_STEP.format(
                url,
                __displayTime__(TIDAL_API.key.authCheckTimeout)
            ),
            disable_web_page_preview=True
        )
        start = time.time()
        elapsed = 0
        while elapsed < TIDAL_API.key.authCheckTimeout:
            elapsed = time.time() - start
            if not TIDAL_API.checkAuthStatus():
                time.sleep(TIDAL_API.key.authCheckInterval + 1)
                continue

            await bot.edit_message_text(
                chat_id=c_id,
                message_id=msg.message.id, 
                text=lang.select.AUTH_SUCCESFULL_MSG.format(
                    __displayTime__(int(TIDAL_API.key.expiresIn))),
                disable_web_page_preview=True,
                reply_markup=tidal_auth_set()
            )

            TOKEN.userid = TIDAL_API.key.userId
            TOKEN.countryCode = TIDAL_API.key.countryCode
            TOKEN.accessToken = TIDAL_API.key.accessToken
            TOKEN.refreshToken = TIDAL_API.key.refreshToken
            TOKEN.expiresAfter = time.time() + int(TIDAL_API.key.expiresIn)
            TOKEN.save()
            return True, None

        raise Exception("Login Operation timed out.")
    except Exception as e:
        return False, e

def loginByConfig():
    try:
        if aigpy.string.isNull(TOKEN.accessToken):
            return False, None
        # If token is valid, return True
        if TIDAL_API.verifyAccessToken(TOKEN.accessToken):
            msg = lang.select.ALREADY_AUTH.format(
                __displayTime__(int(TOKEN.expiresAfter - time.time())))

            TIDAL_API.key.countryCode = TOKEN.countryCode
            TIDAL_API.key.userId = TOKEN.userid
            TIDAL_API.key.accessToken = TOKEN.accessToken
            return True, msg
        # If token is not valid but refresh token is, refresh token and return True
        if TIDAL_API.refreshAccessToken(TOKEN.refreshToken):
            msg = lang.select.ALREADY_AUTH.format(
                __displayTime__(int(TIDAL_API.key.expiresIn)))

            TOKEN.userid = TIDAL_API.key.userId
            TOKEN.countryCode = TIDAL_API.key.countryCode
            TOKEN.accessToken = TIDAL_API.key.accessToken
            TOKEN.expiresAfter = time.time() + int(TIDAL_API.key.expiresIn)
            TOKEN.save()
            return True, msg
        else:
            TokenSettings().save()
            return False, None
    except Exception as e:
        return False, None

async def checkLogin():
    db_auth, _ = set_db.get_variable("AUTH_DONE")
    if not db_auth:
        return False, lang.select.NO_AUTH
    auth, msg = loginByConfig()
    if auth:
        return True, msg
    else:
        return False, lang.select.NO_AUTH

'''
=================================
START DOWNLOAD
=================================
'''
async def start(string, bot, msg, c_id, r_id, u_id):
    strings = string.split(" ")
    for item in strings:
        if aigpy.string.isNull(item):
            continue
        try:
            etype, obj = TIDAL_API.getByString(item)
        except Exception as e:
            LOGGER.warning(str(e) + " [" + item + "]")
            return

        try:
            await start_type(etype, obj, bot, msg, c_id, r_id, u_id)
        except Exception as e:
            LOGGER.warning(str(e))

async def start_type(etype: Type, obj, bot, msg, c_id, r_id, u_id):
    if etype == Type.Album and Config.SEARCH_CHANNEL:
        check = await check_duplicate(obj.title, obj.artist.name, obj.id, bot, c_id, r_id, etype)
        if check:
            return
    if etype == Type.Album:
        await start_album(obj, bot, msg, c_id, r_id, u_id)
    elif etype == Type.Track:
        await start_track(obj, bot, msg, c_id, r_id, u_id)
    elif etype == Type.Artist:
        await start_artist(obj, bot, msg, c_id, r_id, u_id)
    elif etype == Type.Playlist:
        await start_playlist(obj, bot, msg, c_id, r_id, u_id)
    elif etype == Type.Mix:
        await start_mix(obj, bot, msg, c_id, r_id, u_id)

async def start_mix(obj: Mix, bot, msg, c_id, r_id, u_id):
    for index, item in enumerate(obj.tracks):
        album = TIDAL_API.getAlbum(item.album.id)
        item.trackNumberOnPlaylist = index + 1
        await postCover(album, bot, c_id, r_id)
        await downloadTrack(item, album, bot=bot, c_id=c_id, r_id=r_id, u_id=u_id)

async def start_playlist(obj: Playlist, bot, msg, c_id, r_id, u_id):
    tracks, videos = TIDAL_API.getItems(obj.uuid, Type.Playlist)

    for index, item in enumerate(tracks):
        album = TIDAL_API.getAlbum(item.album.id)
        item.trackNumberOnPlaylist = index + 1
        #await postCover(album, bot, c_id, r_id)
        await downloadTrack(item, album, obj, bot=bot, c_id=c_id, r_id=r_id, u_id=u_id)

async def start_artist(obj: Artist, bot, msg, c_id, r_id, u_id):
    albums = TIDAL_API.getArtistAlbums(obj.id, SETTINGS.includeEP)
    for item in albums:
        await start_album(item, bot, msg, c_id, r_id, u_id)

async def start_track(obj: Track, bot, msg, c_id, r_id, u_id):
    album = TIDAL_API.getAlbum(obj.album.id)
    await downloadTrack(obj, album, bot=bot, c_id=c_id, r_id=r_id, u_id=u_id)

async def start_album(obj: Album, bot, msg, c_id, r_id, u_id):
    tracks, videos = TIDAL_API.getItems(obj.id, Type.Album)
    await postCover(obj, bot, c_id, r_id)
    await downloadTracks(tracks, obj, None, bot, c_id, r_id, u_id)
    """for item in tracks:
        await downloadTrack(item, obj, bot=bot, msg=msg, c_id=c_id, r_id=r_id, u_id=u_id)"""

'''
=================================
TIDAL API CHECKS
=================================
'''

async def checkAPI():
    if not apiKey.isItemValid(SETTINGS.apiKeyIndex):
        LOGGER.warning(lang.select.ERR_API_KEY)
    else:
        index = SETTINGS.apiKeyIndex
        TIDAL_API.apiKey = apiKey.getItem(index)

async def getapiInfo():
    i = 0
    platform = []
    validity = []
    quality = []
    index = []
    list = apiKey.__API_KEYS__
    for item in list['keys']:
        index.append(i)
        platform.append(item['platform'])
        validity.append(item['valid'])
        quality.append(item['formats'])
        i += 1
    return index, platform, validity, quality
