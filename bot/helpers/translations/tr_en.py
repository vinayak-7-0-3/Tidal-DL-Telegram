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

Click Commands Button to see available commands.
"""

    CMD_LIST = """
<b>Hello {0} Sir</b>,

The commands for the bot are described below:

<code>/{1}</code> - Shows help message.
<code>/{2}</code> - Downloads the song from Tidal Link.
<code>/{3}</code> - Authenticates the bot in the chat<b>[ADMIN ONLY]</b>.
<code>/{4}</code> - Runs a shell command <b>[ADMIN ONLY]</b>.
<code>/{5}</code> - Open Settings Panel of Bot. <b>[ADMIN ONLY]</b>.

Help for each command is in shown when you type the command.

Feel free to ask doubts in Discussion Group.
"""

    INIT_DOWNLOAD = "Trying to initialize download..."
    FILE_EXIST = "File already exist in the channel.\n\nTitle : <code>{}</code>\n\nClick below to get file."
    ALREADY_AUTH = "Your authentication is already done.\nIts is valid for {}"
    NO_AUTH = "AUTH DISABLED"
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
    TIDAL_AUTH_PANEL = "<b>Configure Tidal Authentication\n\nAuth Status : </b>{}"
    AUTH_SUCCESFULL_MSG = "Authentication successful.\n\nIt is now valid for {}"
    WARN_REMOVE_AUTH = "<b>You are about to remove authentication.</b>\n\nPress again to confirm."
    AUTH_NEXT_STEP = "Go to {} within the next {} to complete setup."
    REMOVED_AUTH_TIDAL = "Removed Tidal Login Successfully"
    CHANGE_QUALITY = "<b>Click to set the quality\n\nCurrent Quality :</b> <code>{}</code>"
    WRONG_USER_CLICK = "You are not allowed to click this button."
    SELECT_API_KEY = """
<b><u>API KEY SETTING PANEL</u></b>
Current API Platform : <code>{0}</code>
Available Formats : <code>{1}</code>
API Key Valid : <code>{2}</code>

<b><u>API PLATFORM INFO</u></b>
{3}
<b>RELOGIN NEEDED AFTER CHANGING API PLATFORM</b>
"""
    API_KEY_CHANGED = "API Key Changed Successfully To - {} - {}\nNow Relogin Tidal for the new api to work."
#
#
# INDEXING
#
#
    INIT_INDEX = "Initializing indexing...\nThis may take a while."
    INDEX_DONE = "Indexing done."
#
#
# BUTTONS
#
#
    JOIN_MUSIC_STORAGE = "Join Music Storage"
    GET_FILE = "Get File"
    LOGIN_TIDAL = "Click To Login"
    TG_AUTH = "TG AUTHS"
    TIDAL_AUTH = "TIDAL AUTH"
    CLOSE = "CLOSE"
    REMOVE_TIDAL_AUTH = "Remove Auth"
    ADD_TIDAL_AUTH = "Add Auth"
    MAIN_MENU = "MAIN MENU"
    COMMANDS = "COMMANDS"
    BOT_LANGUAGE = "BOT LANGUAGE"
    TIDAL_QUALITY = "TIDAL QUALITY - {}"
    TIDAL_QUALITY_HIFI = "HIFI"
    TIDAL_QUALITY_HIGH = "HIGH"
    TIDAL_QUALITY_MASTER = "MASTER"
    TIDAL_QUALITY_NORMAL = "NORMAL"
    # INLINE BUTTONS
    SEARCH_AGAIN = "Search Again"
    MUSIC_C_JOIN = "Join Music Storage"
    LINK = "Link"
    SEARCH = "Search"
    API_KEY_BUTTON = "API KEY"

#
#
# ERRORS
#
#
    ERR_VARS = "Required Variables Missing......\nPlease check everything again."
    ERR_AUTH_CHECK = "Couldn't download because : {}"
    ERR_NO_LINK = "No link found in message."
    ERR_INDEX = "Error while indexing.\n\n{}"
    ERR_API_KEY = "API Key Deprecated. Please change your API Key Index."