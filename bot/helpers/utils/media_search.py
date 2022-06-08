from bot import Config, USER
from bot.helpers.database.postgres_impl import music_db

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

async def check_file_exist_db(title, out=False):
    result = music_db.get_music_id(title)
    if result:
        if out:
            msg = await USER.get_messages(chat_id=Config.SEARCH_CHANNEL, message_ids=result)
            return msg.link
        return True
    else:
        return False

async def index_audio_files(chat_id):
    async for message in USER.search_messages(chat_id=Config.SEARCH_CHANNEL, filter=enums.MessagesFilter.AUDIO):
        if message.audio:
            if not await check_file_exist_db(message.audio.title):
                music_db.set_music(message.id, message.audio.title)

async def check_post_tg(title):
    print(title)
    async for message in USER.search_messages(chat_id=Config.SEARCH_CHANNEL, limit=50, query=title):
        if message.id:
            return message.link