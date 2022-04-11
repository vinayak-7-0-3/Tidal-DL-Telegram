from bot import CMD
from pyrogram import Client, filters
from tidal_dl.util import CONF, TOKEN
from bot.helpers.translations import lang
from bot.helpers.utils.auth_check import check_id
from tidal_dl.download import start as tidal_dl_start
from bot.helpers.database.postgres_impl import TidalSettings

set_db = TidalSettings()

@Client.on_message(filters.command(CMD.DOWNLOAD))
async def download_tidal(bot, update):
    if check_id(message=update):
        try:
            if update.reply_to_message:
                link = update.reply_to_message.text
                reply_to_id = update.reply_to_message.message_id
            else:
                link = update.text.split(" ", maxsplit=1)[1]
                reply_to_id = update.message_id
        except:
            link = None
        if link:
            msg = await bot.send_message(
                chat_id=update.chat.id,
                text=lang.INIT_DOWNLOAD,
                reply_to_message_id=update.message_id
            )
            botmsg_id = msg.message_id
            await tidal_dl_start(TOKEN, CONF, link, bot, update.chat.id, reply_to_id)
            await bot.delete_messages(
                chat_id=update.chat.id,
                message_ids=msg.message_id
            )
        else:
            await bot.send_message(
                chat_id=update.chat.id,
                text=lang.ERR_NO_LINK,
                reply_to_message_id=update.message_id
            )
