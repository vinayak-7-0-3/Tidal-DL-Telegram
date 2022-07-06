from bot import CMD
from pyrogram import Client, filters
from bot.helpers.translations import lang
from bot.helpers.utils.auth_check import check_id
from bot.helpers.utils.auth_check import get_chats
from bot.helpers.buttons.settings_buttons import *
from bot.helpers.tidal_func.settings import SETTINGS
from bot.helpers.database.postgres_impl import set_db, user_settings

import bot.helpers.tidal_func.apikey as apiKey

from bot.helpers.tidal_func.events import checkAPI, checkLogin, getapiInfo, loginByWeb

@Client.on_message(filters.command(CMD.SETTINGS))
async def settings(bot, update):
    if check_id(update.from_user.id, restricted=True):
        await bot.send_message(
            chat_id=update.chat.id,
            text=lang.select.INIT_SETTINGS_MENU,
            reply_markup=main_menu_set()
        )
    else:
        quality = user_settings.get_var(update.from_user.id, "QUALITY")
        if not quality:
            quality = str(SETTINGS.audioQuality).replace("AudioQuality.", "")
        await bot.send_message(
            chat_id=update.chat.id,
            text=lang.select.INIT_SETTINGS_MENU,
            reply_markup=user_set_buttons(quality, update.from_user.id)
        )

@Client.on_callback_query(filters.regex(pattern=r"^tg_panel"))
async def tg_panel_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        msg = await get_chats(True)
        await bot.edit_message_text(
            chat_id=update.message.chat.id,
            message_id=update.message.id,
            text=msg,
            reply_markup=tg_auth_set()
        )


@Client.on_callback_query(filters.regex(pattern=r"^tidal_panel"))
async def tidal_panel_cb(bot, update):
    auth, msg = await checkLogin()
    await bot.edit_message_text(
        chat_id=update.message.chat.id,
        message_id=update.message.id,
        text=lang.select.TIDAL_AUTH_PANEL.format(msg),
        reply_markup=tidal_auth_set()
    )

@Client.on_callback_query(filters.regex(pattern=r"^tiset_warn_auth"))
async def tiset_warn_auth_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        await bot.edit_message_text(
            chat_id=update.message.chat.id,
            message_id=update.message.id,
            text=lang.select.WARN_REMOVE_AUTH,
            reply_markup=tidal_auth_set(True)
        )

@Client.on_callback_query(filters.regex(pattern=r"^tiset_remove_auth"))
async def tiset_remove_auth_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        set_db.set_variable("AUTH_TOKEN", 0, True, None)
        set_db.set_variable("AUTH_DONE", False, False, None)
        try:
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.id,
                text=lang.select.REMOVED_AUTH_TIDAL,
                reply_markup=tidal_auth_set()
            )
        except:
            pass

@Client.on_callback_query(filters.regex(pattern=r"^tiset_add_auth"))
async def tiset_add_auth_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        c_id = update.message.chat.id
        await loginByWeb(bot, update, c_id)
        set_db.set_variable("AUTH_DONE", True, False, None)

@Client.on_callback_query(filters.regex(pattern=r"^close"))
async def close_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        try:
            await bot.delete_messages(
                chat_id=update.message.chat.id,
                message_ids=update.message.id
            )
        except:
            pass
    try:
        if int(update.data.split("_")[1]) == update.from_user.id:
            await bot.delete_messages(
                chat_id=update.message.chat.id,
                message_ids=update.message.id
            )
        else:
            await update.answer(lang.select.WRONG_USER_CLICK)
    except:
        pass

@Client.on_callback_query(filters.regex(pattern=r"^main_menu"))
async def main_menu_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        try:
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.id,
                text=lang.select.INIT_SETTINGS_MENU,
                reply_markup=main_menu_set()
            )
        except:
            pass

@Client.on_callback_query(filters.regex(pattern=r"^tidalq"))
async def tquality_user_cb(bot, update):
    u_id = update.data.split("_")[1]
    quality = update.data.split("_")[2]
    if not int(u_id) == update.from_user.id:
        await update.answer(lang.select.WRONG_USER_CLICK)
        return
    await bot.edit_message_text(
        chat_id=update.message.chat.id,
        message_id=update.message.id,
        text=lang.select.CHANGE_QUALITY.format(quality),
        reply_markup=quality_set(u_id)
    )

@Client.on_callback_query(filters.regex(pattern=r"^setq"))
async def set_tquality_cb(bot, update):
    u_id = update.data.split("_")[2]
    quality = update.data.split("_")[1]
    if not int(u_id) == update.from_user.id:
        await update.answer(lang.select.WRONG_USER_CLICK)
        return
    user_settings.set_var(u_id, "QUALITY", quality)
    await bot.edit_message_text(
        chat_id=update.message.chat.id,
        message_id=update.message.id,
        text=lang.select.CHANGE_QUALITY.format(quality),
        reply_markup=user_set_buttons(quality, u_id)
    )
    
@Client.on_callback_query(filters.regex(pattern=r"^api_panel"))
async def api_panel_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        index, platform, validity, quality = await getapiInfo()
        info = ""
        for number in index:
            info += f"<b>● {number} - {platform[number]}</b>\nFormats - <code>{quality[number]}</code>\nValid - <code>{validity[number]}</code>\n"

        c_index = SETTINGS.apiKeyIndex 
        await bot.edit_message_text(
            chat_id=update.message.chat.id,
            message_id=update.message.id,
            text=lang.select.SELECT_API_KEY.format(
                apiKey.getItem(c_index)['platform'],
                apiKey.getItem(c_index)['formats'],
                apiKey.getItem(c_index)['valid'],
                info
            ),
            reply_markup=api_key_set(index, platform)
        )

@Client.on_callback_query(filters.regex(pattern=r"^setapi"))
async def set_api_cb(bot, update):
    if check_id(update.from_user.id, restricted=True):
        index = int(update.data.split("_")[1])
        set_db.set_variable("API_KEY_INDEX", index, False, None)
        await update.answer(lang.select.API_KEY_CHANGED.format(
            index,
            apiKey.getItem(index)['platform'],
            )
        )
        SETTINGS.read("./.tidal-dl.json")
        await checkAPI()
        try:
            await api_panel_cb(bot, update)
        except:
            pass
    