from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def cmds_button():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="COMMANDS",
                callback_data="cmdscb"
            ),
            InlineKeyboardButton(
                text="CLOSE",
                callback_data="close"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)