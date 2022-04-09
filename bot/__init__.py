import logging
from config import Config
from pyrogram import Client

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
LOGGER = logging.getLogger(__name__)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("hachoir").setLevel(logging.WARNING)
logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("charset_normalizer").setLevel(logging.WARNING)

bot = Config.BOT_USERNAME

class CMD(object):
    START = ["start", f"start@{bot}"]
    HELP = ["help", f"help@{bot}"]
    # List out all the commands
    CMD_LIST = ["cmds", f"cmds@{bot}"]
    # Open Settings Panel - TODO
    SETTINGS = ["settings", f"settings@{bot}"]

    DOWNLOAD = ["download", f"download@{bot}"]

    # Auth user or chat to use the bot
    # TODO Add cmd to remove auth
    AUTH = ["auth", f"auth@{bot}"]
    # AUTH TIDAL
    AUTH_TIDAL = ["auth_tidal", f"auth_tidal@{bot}"]
    # Add user as admin user
    ADD_ADMIN = ["add_sudo", f"add_sudo@{bot}"]
    # To execute shell cmds
    SHELL = ["shell", f"shell@{bot}"]
    # Shows List Of Authed Chats
    AUTHED_CHATS = ["authed", f"authed@{bot}"]

USER = Client(
    session_name=Config.USER_SESSION,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH
)