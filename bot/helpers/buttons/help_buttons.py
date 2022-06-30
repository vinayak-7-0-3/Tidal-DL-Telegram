from bot.helpers.translations import lang
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def cmds_button():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.COMMANDS,
                callback_data="cmdscb"
            ),
            InlineKeyboardButton(
                text=lang.CLOSE,
                callback_data="close"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)