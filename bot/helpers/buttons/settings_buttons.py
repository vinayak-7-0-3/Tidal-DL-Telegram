from bot.helpers.translations import lang
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

exit_button = [InlineKeyboardButton(text=lang.select.MAIN_MENU, callback_data="main_menu"),
                InlineKeyboardButton(text=lang.select.CLOSE, callback_data="close")]

def main_menu_set():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.select.TG_AUTH,
                callback_data="tg_panel"
            ),
            InlineKeyboardButton(
                text=lang.select.TIDAL_AUTH,
                callback_data="tidal_panel"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.API_KEY_BUTTON,
                callback_data="api_panel"
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.CLOSE,
                callback_data="close"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)

def tidal_auth_set(final=False):
    if final:
        button2 = InlineKeyboardButton(
            text=lang.select.REMOVE_TIDAL_AUTH,
            callback_data="tiset_remove_auth"
        )
    else:
        button2 = InlineKeyboardButton(
            text=lang.select.REMOVE_TIDAL_AUTH,
            callback_data="tiset_warn_auth"
        )
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.select.ADD_TIDAL_AUTH,
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

def user_set_buttons(t_q, user_id):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.select.TIDAL_QUALITY.format(t_q),
                callback_data="tidalq_" + str(user_id) + "_" + str(t_q)
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.CLOSE,
                callback_data="close_" + str(user_id)
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)

def quality_set(u_id):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=lang.select.TIDAL_QUALITY_MASTER,
                callback_data="setq_Master_" + str(u_id)
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.TIDAL_QUALITY_HIFI,
                callback_data="setq_HiFi_" + str(u_id)
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.TIDAL_QUALITY_NORMAL,
                callback_data="setq_Normal_" + str(u_id)
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.TIDAL_QUALITY_HIGH,
                callback_data="setq_High_" + str(u_id)
            )
        ],
        [
            InlineKeyboardButton(
                text=lang.select.CLOSE,
                callback_data="close_" + str(u_id)
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)

def api_key_set(index, platform):
    inline_keyboard = []
    for i in index:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=f"{i} - {platform[i]}",
                callback_data=f"setapi_{i}"
                )
            ]
        )
    inline_keyboard.append(exit_button)
    return InlineKeyboardMarkup(inline_keyboard)