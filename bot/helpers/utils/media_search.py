from pyrogram import enums
from bot import Config, USER, LOGGER
from bot.helpers.translations import lang
from bot.helpers.tidal_func.enums import Type
from bot.helpers.database.postgres_impl import music_db

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def search_media_audio(query):
    title = []
    artist = []
    thumb = []
    link = []
    async for message in USER.search_messages(chat_id=Config.SEARCH_CHANNEL, limit=50, query=query, filter=enums.MessagesFilter.AUDIO):
        if message.audio:
            title.append(message.audio.title)
            artist.append(message.audio.performer)
            thumb.append(message.audio.thumbs)
            link.append(message.link)
    return title, artist, link

async def check_file_exist_db(bot, title, artist, out=False):
    r_id, r_artist = music_db.get_music_id(title, artist)
    if r_id:
        if artist == r_artist:
            if out:
                msg = await bot.get_messages(chat_id=Config.SEARCH_CHANNEL, message_ids=r_id)
                return msg.link
            return True
    else:
        return False

async def index_audio_files(chat_id):
    async for message in USER.search_messages(chat_id=Config.SEARCH_CHANNEL, filter=enums.MessagesFilter.AUDIO):
        if message.audio:
            if not await check_file_exist_db(None, message.audio.title, message.audio.performer):
                music_db.set_music(message.id, message.audio.title, message.audio.performer)

async def check_post_tg(title):
    if Config.USER_SESSION is not None and Config.USER_SESSION != "":
        async for message in USER.search_messages(chat_id=Config.SEARCH_CHANNEL, limit=50, query=title):
            if message.id:
                return message.link
    else:
        LOGGER.info("No User Session Provided. Skipping Duplicate Check...")
        return False

async def check_duplicate(title, artist, bot, c_id, r_id, etype=None):
    try:
        if etype == Type.Album:
            msg_link = await check_post_tg(title)
        else:
            msg_link = await check_file_exist_db(bot, title, artist, True)
        if msg_link:
            inline_keyboard = []
            inline_keyboard.append([InlineKeyboardButton(text=lang.select.GET_FILE, url=msg_link)])
            if not Config.MUSIC_CHANNEL_LINK == "":
                inline_keyboard.append([InlineKeyboardButton(text=lang.select.JOIN_MUSIC_STORAGE, url=Config.MUSIC_CHANNEL_LINK)])
            await bot.send_message(
                chat_id=c_id,
                text=lang.select.FILE_EXIST.format(title),
                reply_to_message_id=r_id,
                reply_markup=InlineKeyboardMarkup(inline_keyboard)
            )
            LOGGER.info(title + " already exist")
            return True
    except Exception as e:
        LOGGER.warning(e)