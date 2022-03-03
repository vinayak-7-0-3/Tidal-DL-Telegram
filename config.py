class Config_NONENV(object):
    TG_BOT_TOKEN = ""
    APP_ID = 1342083
    API_HASH = ""
    USER_SESSION = ""

    AUTH_CHAT = "123 123"
    ADMINS = "123 123"

    LOG_CHANNEL_ID = 1223
    ALLOW_DUMP = "False"
    SEARCH_CHANNEL = -100

    IS_BOT_PUBLIC = False
    AUTH_USERS = ""

    WORK_DIR = "./bot/"
    DOWNLOADS_FOLDER = "DOWNLOADS"
    DOWNLOAD_BASE_DIR = WORK_DIR + DOWNLOADS_FOLDER

    INLINE_THUMB = None
    # Country code for Tidal API (in caps)
    # Default values are recommended
    TIDAL_REGION = "IN"
    TIDAL_SEARCH_LIMIT = 10

    BOT_USERNAME = ""
    OWNER_USERNAME = ""

    DATABASE_URL = ""
#
#
#
#
#   RESTRICTED AREA XD
#
#
#
# 
    ADMINS = set(int(x) for x in ADMINS.split(" "))
    AUTH_CHAT = set(int(x) for x in AUTH_CHAT.split(" "))
    if AUTH_USERS:
        AUTH_USERS = set(int(x) for x in AUTH_USERS.split(" "))

    if BOT_USERNAME.startswith("@"):
        BOT_USERNAME = BOT_USERNAME[1:]
    if OWNER_USERNAME.startswith("@"):
        OWNER_USERNAME = OWNER_USERNAME[1:]