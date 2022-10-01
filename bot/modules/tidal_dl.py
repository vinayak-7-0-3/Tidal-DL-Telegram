from bot import CMD
from config import LOGGER, Config
from pyrogram import Client, filters

from bot.helpers.translations import lang
from bot.helpers.utils.auth_check import check_id
from bot.helpers.utils.check_link import check_link
from bot.helpers.tidal_func.events import checkLogin, start
from bot.helpers.database.postgres_impl import user_settings

@Client.on_message(filters.command(CMD.DOWNLOAD))
async def download_tidal(bot, update):
    if await check_id(message=update):
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

            if update.from_user.username:
                u_name = f"@{update.from_user.username}"
            else:
                u_name = f'<a href="tg://user?id={update.from_user.id}">{update.from_user.first_name}</a>'

            auth, err = await checkLogin()
            if auth:
                user_settings.set_var(update.chat.id, "ON_TASK", True)
                await start(link, bot, update, update.chat.id, reply_to_id, update.from_user.id, u_name)
                user_settings.set_var(update.chat.id, "ON_TASK", False)
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
            await bot.send_message(
                chat_id=update.chat.id,
                text=lang.select.DOWNLOAD_DONE,
                reply_to_message_id=reply_to_id
            )
        else:
            await bot.send_message(
                chat_id=update.chat.id,
                text=lang.select.ERR_NO_LINK,
                reply_to_message_id=update.id
            )
