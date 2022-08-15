from bot import CMD
from config import LOGGER, Config
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.utils.auth_check import check_id
from bot.helpers.utils.check_link import check_link
from bot.helpers.tidal_func.events import checkLogin, start

@Client.on_message(filters.command(CMD.DOWNLOAD))
async def download_tidal(bot, update):
    if check_id(message=update):
        try:
            if update.reply_to_message:
                link = update.reply_to_message.text
                reply_to_id = update.reply_to_message.id
            else:
                link = update.text.split(" ", maxsplit=1)[1]
                reply_to_id = update.id
            if Config.ALLOW_OTHER_LINKS == "True":
                link = await check_link(link)
        except:
            link = None

        if link:
            LOGGER.info(f"Download Initiated By - {update.from_user.first_name}")
            msg = await bot.send_message(
                chat_id=update.chat.id,
                text=lang.select.INIT_DOWNLOAD,
                reply_to_message_id=update.id
            )
            botmsg_id = msg.id
            auth, err = await checkLogin()
            if auth:
                await start(link, bot, update, update.chat.id, reply_to_id, update.from_user.id)
            else:
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    message_id=botmsg_id,
                    text=lang.select.ERR_AUTH_CHECK.format(err),
                )
                return
        
            await bot.delete_messages(
                chat_id=update.chat.id,
                message_ids=msg.id
            )
        else:
            await bot.send_message(
                chat_id=update.chat.id,
                text=lang.select.ERR_NO_LINK,
                reply_to_message_id=update.id
            )
