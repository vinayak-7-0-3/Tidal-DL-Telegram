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

async def check_file_exist_db(bot, title, out=False):
    result = music_db.get_music_id(title)
    if result:
        if out:
            msg = await bot.get_messages(chat_id=Config.SEARCH_CHANNEL, message_ids=result)
            return msg.link
        return True
    else:
        return False

async def index_audio_files(chat_id):
    async for message in USER.search_messages(chat_id=Config.SEARCH_CHANNEL, filter=enums.MessagesFilter.AUDIO):
        if message.audio:
            if not await check_file_exist_db(None, message.audio.title):
                music_db.set_music(message.id, message.audio.title)

async def check_post_tg(title):
    async for message in USER.search_messages(chat_id=Config.SEARCH_CHANNEL, limit=50, query=title):
        if message.id:
            return message.link

async def check_duplicate(title, bot, c_id, r_id, etype=None):
    try:
        if etype == Type.Album:
            msg_link = await check_post_tg(title)
        else:
            msg_link = await check_file_exist_db(bot, title, True)
        if msg_link:
            inline_keyboard = []
            inline_keyboard.append([InlineKeyboardButton(text=lang.GET_FILE, url=msg_link)])
            if not Config.MUSIC_CHANNEL_LINK == "":
                inline_keyboard.append([InlineKeyboardButton(text=lang.JOIN_MUSIC_STORAGE, url=Config.MUSIC_CHANNEL_LINK)])
            await bot.send_message(
                chat_id=c_id,
                text=lang.FILE_EXIST.format(title),
                reply_to_message_id=r_id,
                reply_markup=InlineKeyboardMarkup(inline_keyboard)
            )
            LOGGER.info(title + " already exist")
            return True
    except Exception as e:
        LOGGER.warning(e)