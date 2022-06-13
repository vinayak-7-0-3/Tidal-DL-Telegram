class EN(object):
    INIT_MSG = "<b>Hello {} Sir</b>"

    START_TEXT = """
<b>Hello {} Sir</b>,
Iam a Tidal DL Bot. Used to download songs from Tidal.
"""

    HELP_MSG = """
<b>Hello {} Sir</b>,

Iam a Tidal DL Bot. Used to download songs from tidal.com.

You can download all songs at master quality.

See <code>/{}</code> for commands.
"""

    CMD_LIST = """
<b>Hello {0} Sir</b>,

The commands for the bot are described below:

<code>/{1}</code> - Shows help message.
<code>/{2}</code> - Shows the list of commands.
<code>/{3}</code> - Downloads the song from Tidal Link.
<code>/{4}</code> - Authenticates the bot in the chat<b>[ADMIN ONLY]</b>.
<code>/{5}</code> - Runs a shell command <b>[ADMIN ONLY]</b>.
<code>/{6}</code> - Open Settings Panel of Bot. <b>[ADMIN ONLY]</b>.

Help for each command is in shown when you type the command.

Feel free to ask doubts in Discussion Group.
"""

    INIT_DOWNLOAD = "Trying to initialize download..."
    ERR_NO_LINK = "No link found in message."
    FILE_EXIST = "File already exist in the channel.\n\nTitle : <code>{}</code>\n\nClick below to get file."

    ALREADY_AUTH = "Your authentication is already done.\nIts is valid for {}"
    AUTH_DISABLED = "Cannot download because authentication is disabled."
#
#
# INLINE MODE TEXTS..............................................................
#
#
    INLINE_SEARCH_HELP = """
Use can use this bot to search for songs direclty anywhere.

Use flags along with the search query to get the results.

Flags are :
<code>-s</code> for track from tidal
<code>-a</code> for album from tidal
<code>-d</code> song from dump channel
"""
    INLINE_PLACEHOLDER = "Click here for the help with search."
    INLINE_NO_RESULT = "No results found"

    INPUT_MESSAGE_TRACK = """
💽 <b>Title :</b> {0}
👤 <b>Artist :</b> {1}
💿 <b>Album :</b> {2}
🕒 <b>Duration :</b> {3}
"""

    INPUT_MESSAGE_ALBUM = """
💽 <b>Title :</b> {0}
👤 <b>Artist :</b> {1}
📀 <b>Tracks :</b> {2}
📅 <b>Release Date :</b> {3}
"""

    INLINE_MEDIA_SEARCH = """
<b>Title :</b> {0}

<b>Artist :</b> {1}
"""
#
#
# ALBUM TEXT FORMAT...............................................................
#
#
    ALBUM_DETAILS = """
💽 <b>Title :</b> {0}
👤 <b>Artist :</b> {1}
📅 <b>Release Date :</b> {2}
📀 <b>Number of Tracks :</b> {3}
🕒 <b>Duration :</b> {4}
🔢 <b>Number of Volumes :</b> {5}
"""
#
#
# CHATS AUTH MSGS
#
#
    CHAT_AUTH = "Authorised the chat : {} successfully."
    ADD_ADMIN = "Added {} as admin user."
    NO_ID_PROVIDED = "No ID provided to add admin.\nReply to a person's message or provide the ID with the command."
#
#
# SETTINGS PANEL
#
#
    INIT_SETTINGS_MENU = "<b>Welcome to Bot Settings Menu.</b>\n\nChoose the option to open its settings."
    TIDAL_AUTH_PANEL = "<b>Configure Tidal Authentication</b>\n\n"
    AUTH_SUCCESFULL_MSG = "Authentication successful.\n\n"
    WARN_REMOVE_AUTH = "<b>You are about to remove authentication.</b>\n\nPress again to confirm."
#
#
# INDEXING
#
#
    INIT_INDEX = "Initializing indexing...\nThis may take a while."
    ERR_INDEX = "Error while indexing.\n\n{}"
    INDEX_DONE = "Indexing done.\nTotal Files : {}"
    ERR_NO_CHANNEL = "No channel found to index.\nPlease check you ENV variables"
