from config import Config
from bot.helpers.translations.tr_en import EN


class Language(object):
    def __init__(self) -> None:
        if Config.BOT_LANGUAGE == "en":
            self.select = EN()
        else:
            self.select = EN()


lang = Language()
