from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

exit_button = [InlineKeyboardButton(text="MAIN MENU", callback_data="main_menu"),
                InlineKeyboardButton(text="CLOSE", callback_data="close")]

def main_menu_set():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="TG AUTHS",
                callback_data="tg_panel"
            ),
            InlineKeyboardButton(
                text="TIDAl AUTH",
                callback_data="tidal_panel"
            )
        ],
        [
            InlineKeyboardButton(
                text="CLOSE",
                callback_data="close"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)

def tidal_auth_set():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Add Auth",
                callback_data="tiset_add_auth"
            ),
            InlineKeyboardButton(
                text="Remove Auth",
                callback_data="tiset_remove_auth"
            )
        ],
        exit_button
    ]
    return InlineKeyboardMarkup(inline_keyboard)

def tg_auth_set():
    inline_keyboard = [
        exit_button
    ]
    return InlineKeyboardMarkup(inline_keyboard)