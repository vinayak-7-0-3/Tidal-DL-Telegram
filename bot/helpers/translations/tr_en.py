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
<code>/{4}</code> - Authenticates the bot <b>[OWNER ONLY]</b>.
<code>/{5}</code> - Runs a shell command <b>[OWNER ONLY]</b>.

Help for each command is in shown when you type the command.

Feel free to ask doubts in Discussion Group.
"""

    INIT_DOWNLOAD = "Trying to initialize download..."
    ERR_NO_LINK = "No link found in message."

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
    INLINE_NOT_AUTH = "You are not authenticated.\nContact @{} for authentication."
    INLINE_NOT_AUTH_MSG = """
You are not authenticated.

Contact @{} for authentication

You can use other search options.
"""

    INPUT_MESSAGE_TRACK = """
<b>Title :</b> {0}

<b>Artist :</b> {1}

<b>Album :</b> {2}

<b>Duration :</b> {3}
"""

    INPUT_MESSAGE_ALBUM = """
<b>Title :</b> {0}

<b>Artist :</b> {1}

<b>Tracks :</b> {2}

<b>Release Date :</b> {3}
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
<b>Title :</b> {0}

<b>Artist :</b> {1}

<b>Release Date :</b> {2}

<b>Number of Tracks :</b> {3}

<b>Duration :</b> {4}

<b>Number of Volumes :</b> {5}
"""
#
#
# CHATS AUTH MSGS
#
#
    CHAT_AUTH = "Authorised the chat : {} successfully."
    ADD_ADMIN = "Added {} as admin user."