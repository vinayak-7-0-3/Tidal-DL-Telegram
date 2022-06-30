from bot.helpers.translations import lang
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

exit_button = [InlineKeyboardButton(text=lang.MAIN_MENU, callback_data="main_menu"),
                InlineKeyboardButton(text=lang.CLOSE, callback_data="close")]

def main_menu_set():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.TG_AUTH,
                callback_data="tg_panel"
            ),
            InlineKeyboardButton(
                text=lang.TIDAL_AUTH,
                callback_data="tidal_panel"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.CLOSE,
                callback_data="close"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)

def tidal_auth_set(final=False):
    if final:
        button2 = InlineKeyboardButton(
            text=lang.REMOVE_TIDAL_AUTH,
            callback_data="tiset_remove_auth"
        )
    else:
        button2 = InlineKeyboardButton(
            text=lang.REMOVE_TIDAL_AUTH,
            callback_data="tiset_warn_auth"
        )
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.ADD_TIDAL_AUTH,
                callback_data="tiset_add_auth"
            ),
            button2
        ],
        exit_button
    ]
    return InlineKeyboardMarkup(inline_keyboard)

def tg_auth_set():
    inline_keyboard = [
        exit_button
    ]
    return InlineKeyboardMarkup(inline_keyboard)