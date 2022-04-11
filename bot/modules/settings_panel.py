import tidal_dl
from bot import CMD, LOGGER
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.utils.auth_check import check_id
from bot.helpers.utils.auth_check import get_chats
from bot.helpers.buttons.settings_buttons import *
from bot.helpers.database.postgres_impl import TidalSettings

set_db = TidalSettings()

@Client.on_message(filters.command(CMD.SETTINGS))
async def settings(bot, update):
    if check_id(update.from_user.id, restricted=True):
        await bot.send_message(
            chat_id=update.chat.id,
            text=lang.INIT_SETTINGS_MENU,
            parse_mode="html",
            reply_markup=main_menu_set()
        )

@Client.on_callback_query(filters.regex(pattern=r"^tg_panel"))
async def tg_panel_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        msg = await get_chats(True)
        await bot.edit_message_text(
            chat_id=update.message.chat.id,
            message_id=update.message.message_id,
            text=msg,
            reply_markup=tg_auth_set()
        )


@Client.on_callback_query(filters.regex(pattern=r"^tidal_panel"))
async def tidal_panel_cb(bot, update):
    await bot.edit_message_text(
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
        text=lang.TIDAL_AUTH_PANEL,
        reply_markup=tidal_auth_set()
    )

@Client.on_callback_query(filters.regex(pattern=r"^tiset_remove_auth"))
async def tiset_remove_auth_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        set_db.set_variable("AUTH_TOKEN", 0, True, None)
        set_db.set_variable("AUTH_DONE", False, False, None)
        try:
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                text="Removed Tidal Login Successfully",
                reply_markup=tidal_auth_set()
            )
        except:
            pass

@Client.on_callback_query(filters.regex(pattern=r"^tiset_add_auth"))
def tiset_add_auth_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        chat_id = update.message.chat.id
        tidal_dl.checkLogin(bot, chat_id, update, True)
        set_db.set_variable("AUTH_DONE", True, False, None)

@Client.on_callback_query(filters.regex(pattern=r"^close"))
async def close_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        try:
            await bot.delete_messages(
                chat_id=update.message.chat.id,
                message_ids=update.message.message_id
            )
        except:
            pass

@Client.on_callback_query(filters.regex(pattern=r"^main_menu"))
async def main_menu_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        try:
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                text=lang.INIT_SETTINGS_MENU,
                reply_markup=main_menu_set()
            )
        except:
            pass