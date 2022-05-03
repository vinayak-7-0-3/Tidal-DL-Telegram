from bot import Config, USER

async def search_media_audio(query):
    title = []
    artist = []
    thumb = []
    link = []
    async for message in USER.search_messages(chat_id=Config.SEARCH_CHANNEL, limit=50, query=query, filter="audio"):
        if message.audio:
            title.append(message.audio.title)
            artist.append(message.audio.performer)
            thumb.append(message.audio.thumbs)
            link.append(message.link)
    return title, artist, link

async def check_file_exist(title):
    async for message in USER.search_messages(chat_id=Config.SEARCH_CHANNEL, limit=1, query=title, filter="empty"):
        if message:
            return True, message.link
        else:
            return False, None