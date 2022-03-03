import os

class Config_ENV(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    USER_SESSION = os.environ.get("USER_SESSION")

    AUTH_CHAT = set(int(x) for x in os.environ.get("AUTH_CHAT", "").split())
    ADMINS = set(int(x) for x in os.environ.get("ADMINS", "").split())

    LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", 12345))
    ALLOW_DUMP = bool(os.environ.get("ALLOW_DUMP", False))
    SEARCH_CHANNEL = int(os.environ.get("SEARCH_CHANNEL", 12345))
    
    IS_BOT_PUBLIC = bool(os.environ.get("IS_BOT_PUBLIC", False))
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
    
    WORK_DIR = os.environ.get("WORK_DIR", "./bot/")
    DOWNLOADS_FOLDER = os.environ.get("DOWNLOADS_FOLDER", "DOWNLOADS")
    DOWNLOAD_BASE_DIR = WORK_DIR + DOWNLOADS_FOLDER

    INLINE_THUMB = os.environ.get("INLINE_THUMB", "")
    
    # Country code for Tidal API (in caps)
    TIDAL_REGION = os.environ.get("TIDAL_REGION", "")
    TIDAL_SEARCH_LIMIT = int(os.environ.get("TIDAL_SEARCH_LIMIT", 10))
    
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "")

    DATABASE_URL = os.environ.get("DATABASE_URL", "")

    if BOT_USERNAME.startswith("@"):
        BOT_USERNAME = BOT_USERNAME[1:]
    if OWNER_USERNAME.startswith("@"):
        OWNER_USERNAME = OWNER_USERNAME[1:]