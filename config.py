import os
import logging
from os import getenv
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
LOGGER = logging.getLogger(__name__)

if not os.environ.get("ENV"):
    load_dotenv('.env', override=True)

class Config(object):
    try:
        TG_BOT_TOKEN = getenv("TG_BOT_TOKEN")
        APP_ID = int(getenv("APP_ID", 123))
        API_HASH = getenv("API_HASH")
       
    except:
        LOGGER.warning("Essential TG Configs are missing")
        exit(1)

    USER_SESSION = getenv("USER_SESSION", "")

    try:
        AUTH_CHAT = set(int(x) for x in getenv("AUTH_CHAT").split())
    except:
        AUTH_CHAT = ""
    try:
        ADMINS = set(int(x) for x in getenv("ADMINS").split())
    except:
        LOGGER.warning("NO ADMIN USER IDS FOUND")
        exit(1)

    try:
        LOG_CHANNEL_ID = int(getenv("LOG_CHANNEL_ID"))
    except:
        LOG_CHANNEL_ID = None
    ALLOW_DUMP = getenv("ALLOW_DUMP", False)

    try:
        SEARCH_CHANNEL = int(getenv("SEARCH_CHANNEL"))
    except:
        if LOG_CHANNEL_ID:
            SEARCH_CHANNEL = LOG_CHANNEL_ID
        else:
            SEARCH_CHANNEL = None
    
    IS_BOT_PUBLIC = getenv("IS_BOT_PUBLIC", True)

    try:
        AUTH_USERS = set(int(x) for x in getenv("AUTH_USERS").split())
    except:
        AUTH_USERS = ""

    WORK_DIR = getenv("WORK_DIR", "./bot/")
    DOWNLOADS_FOLDER = getenv("DOWNLOADS_FOLDER", "DOWNLOADS")
    DOWNLOAD_BASE_DIR = WORK_DIR + DOWNLOADS_FOLDER

    INLINE_THUMB = getenv("INLINE_THUMB", "")
    
    # Country code for Tidal API (in caps)
    TIDAL_REGION = getenv("TIDAL_REGION", "IN")
    TIDAL_SEARCH_LIMIT = int(getenv("TIDAL_SEARCH_LIMIT", 10))
    
    BOT_USERNAME = getenv("BOT_USERNAME", "")
    if not BOT_USERNAME:
        LOGGER.warning("NO BOT USERNAME FOUND")
        exit(1)
    
    DATABASE_URL = getenv("DATABASE_URL")
    if not DATABASE_URL:
        LOGGER.warning("NO DATABASE URL FOUND")
        exit(1)

    MUSIC_CHANNEL_LINK = getenv("MUSIC_CHANNEL_LINK", "")
    BOT_LANGUAGE = getenv("BOT_LANGUAGE", "en")

    ALLOW_OTHER_LINKS = getenv("ALLOW_OTHER_LINKS", False)

    if BOT_USERNAME.startswith("@"):
        BOT_USERNAME = BOT_USERNAME[1:]
    if ALLOW_DUMP == "True" and USER_SESSION is None:
        LOGGER.warning("You have set ALLOW_DUMP to True but no USER_SESSION provided.")
        exit(1)
    if ALLOW_DUMP == "True" and LOG_CHANNEL_ID == -69:
        LOGGER.warning("You have set ALLOW_DUMP to True but have't provided any LOG_CHANNEL_ID.")
        exit(1)